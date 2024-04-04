import logging

from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
from ray.tune.logger import Logger, pretty_print
import os


class TensorBoardLogger(Logger):
    def __init__(self, config, logdir):
        super().__init__(config, logdir)
        now = "{date:%Y-%m-%d_%H:%M:%S}.log".format(date=datetime.now())
        self._log_file = os.path.join(logdir, "log_" + now)
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(self._log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self.writer = SummaryWriter(log_dir=logdir + "tbf_log_" + now)

    def on_result(self, result, step=None):
        self.last_result = result
        self._logger.debug(pretty_print(result))
        of_interest = [
            "episode_reward_mean",
            "episode_reward_max",
            "episode_reward_min",
            "time_this_iter_s",
        ]
        iter_num = result["training_iteration"]
        self._logger.info("\n\n")
        for key in of_interest:
            self.writer.add_scalar(key, result[key], global_step=iter_num)
            self._logger.info("Episode {}, {} : {}".format(iter_num, key, result[key]))
        self._logger.info("\n\n")

    def on_end(self):
        self.writer.close()


def get_logger(global_config):
    def get_tensorboard_logger(drl_algo_config):
        """Create a logger for Ray."""
        # Define the directory for logging
        logdir = global_config.get("log_dir", None)
        if logdir is None:
            logdir = "./no_dir_given"

        # Configure logging
        logging.basicConfig(level=logging.INFO)

        # Create and return the UnifiedLogger
        return TensorBoardLogger(global_config, logdir)

    return get_tensorboard_logger
