"""Smoke tests for AIRL with ``NormalizedRewardNet``."""

import pytest
import stable_baselines3

from imitation.algorithms.adversarial import airl
from imitation.data import rollout, types
from imitation.rewards import reward_nets
from imitation.util import networks, util


@pytest.fixture
def simple_airl_trainer(cartpole_expert_trajectories, tmp_path, rng):
    venv = util.make_vec_env("seals/CartPole-v0", n_envs=1, parallel=False, rng=rng)
    gen_algo = stable_baselines3.PPO(
        stable_baselines3.common.policies.ActorCriticPolicy,
        venv,
    )
    base = reward_nets.BasicRewardNet(venv.observation_space, venv.action_space)
    reward_net = reward_nets.NormalizedRewardNet(base, networks.RunningNorm)
    trainer = airl.AIRL(
        demonstrations=cartpole_expert_trajectories,
        demo_batch_size=1,
        venv=venv,
        gen_algo=gen_algo,
        reward_net=reward_net,
        log_dir=tmp_path,
    )
    yield trainer
    venv.close()


def test_airl_train_disc(simple_airl_trainer, rng):
    transitions = rollout.generate_transitions(
        policy=simple_airl_trainer.gen_algo,
        venv=simple_airl_trainer.venv,
        n_timesteps=1,
        truncate=True,
        rng=rng,
    )
    simple_airl_trainer.train_disc(
        gen_samples=types.dataclass_quick_asdict(transitions),
    )
