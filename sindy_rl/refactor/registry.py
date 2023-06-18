from gym.envs.mujoco.swimmer_v4 import SwimmerEnv
from ray.rllib.env.wrappers.dm_control_wrapper import DMCEnv

from sindy_rl.refactor.swimmer import SwimmerWithBounds, SwimmerWithBoundsClassic

class DMCEnvWrapper(DMCEnv):
    def __init__(self, config=None):
        env_config = config or {}
        super().__init__(**env_config)
    
    # def reset(self,seed=None):
    #     '''Note, the seed actually does nothing right now. Just to conform to our method'''
    #     return super().reset()