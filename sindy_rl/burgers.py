import controlgym as gym

env = gym.make("convection_diffusion_reaction")


# adapter pattern for the controlgym burgers PDE example to be used in SindyRL
class BurgersControlEnv(gym.envs.BurgersEnv):
    def __init__(self, config=None):
        config = config or {}
        super().__init__(**config)

    def reset(self, **kwargs):
        # return observation and info
        return super(BurgersControlEnv, self).reset(
            seed=kwargs.get("seed", None), state=kwargs.get("state", None)
        )
