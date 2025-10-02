import cProfile
import pstats
import numpy as np
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.evaluation import evaluate_policy
from imitation.algorithms.adversarial.airl import AIRL
from imitation.data import rollout
from imitation.data.wrappers import RolloutInfoWrapper
from imitation.policies.serialize import load_policy
from imitation.rewards.reward_nets import BasicShapedRewardNet
from imitation.util.networks import RunningNorm
from imitation.util.util import make_vec_env

SEED = 42␊
N_ENVS = 8␊
env_id = "HalfCheetah-v4"

def main():
    # （ここまで通常の環境構築部分）
    env = make_vec_env(
        env_id,
        rng=np.random.default_rng(SEED),
        n_envs=N_ENVS,
        post_wrappers=[lambda env, _: RolloutInfoWrapper(env)],
    )
    expert = load_policy(
        "sac-huggingface",
        organization="delta8tyome",
        env_name="seed0-HalfCheetah-v4",
        venv=env,
    )
    rollouts = rollout.rollout(
        expert,
        env,
        rollout.make_sample_until(min_episodes=60),
        rng=np.random.default_rng(SEED),
    )
    learner = PPO(
        env=env,
        policy=MlpPolicy,
        batch_size=512,
        ent_coef=0.0,
        learning_rate=3e-4,
        gamma=0.99,
        clip_range=0.2,
        vf_coef=0.25,
        n_epochs=10,
        seed=SEED,
    )
    reward_net = BasicShapedRewardNet(
        observation_space=env.observation_space,
        action_space=env.action_space,
        normalize_input_layer=RunningNorm,
    )
    airl_trainer = AIRL(
        demonstrations=rollouts,
        demo_batch_size=4096,
        gen_replay_buffer_capacity=4096,
        n_disc_updates_per_round=32,
        venv=env,
        gen_algo=learner,
        reward_net=reward_net,
        log_dir="logs/airl_half_cheetah",
    )
    # 評価前の報酬を取得
    env.seed(SEED)
    learner_rewards_before_training, _ = evaluate_policy(
        learner, env, n_eval_episodes=20, return_episode_rewards=True
    )
    # AIRL 学習開始
    airl_trainer.train(2_000_000)
    # 学習後の評価
    env.seed(SEED)
    learner_rewards_after_training, _ = evaluate_policy(
        learner, env, n_eval_episodes=20, return_episode_rewards=True
    )
    print("Mean reward before AIRL:", np.mean(learner_rewards_before_training))
    print("Mean reward after  AIRL:", np.mean(learner_rewards_after_training))

if __name__ == "__main__":
    # cProfile で main() を丸ごとプロファイリングし、結果を out.prof に保存する
    cProfile.run("main()", filename="out.prof")
