[![CircleCI](https://circleci.com/gh/HumanCompatibleAI/imitation.svg?style=svg)](https://circleci.com/gh/HumanCompatibleAI/imitation)
[![Documentation Status](https://readthedocs.org/projects/imitation/badge/?version=latest)](https://imitation.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/HumanCompatibleAI/imitation/branch/master/graph/badge.svg)](https://codecov.io/gh/HumanCompatibleAI/imitation)
[![PyPI version](https://badge.fury.io/py/imitation.svg)](https://badge.fury.io/py/imitation)

# 模倣学習のベースライン実装

このプロジェクトは模倣学習および報酬学習アルゴリズムを明快に実装することを目指しています。
現在、以下のアルゴリズムが実装されています。「離散」「連続」は、それぞれ離散または連続の行動/状態空間をサポートするかどうかを表します。

| アルゴリズム (+ 論文リンク)                                                                                                        | APIドキュメント                                                                                                                | 離散 | 連続 |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -- | -- |
| 行動クローニング（Behavioral Cloning）                                                                                            | [`algorithms.bc`](https://imitation.readthedocs.io/en/latest/algorithms/bc.html)                                         | ✅  | ✅  |
| [DAgger](https://arxiv.org/pdf/1011.0686.pdf)                                                                           | [`algorithms.dagger`](https://imitation.readthedocs.io/en/latest/algorithms/dagger.html)                                 | ✅  | ✅  |
| 密度ベースの報酬モデル                                                                                                             | [`algorithms.density`](https://imitation.readthedocs.io/en/latest/algorithms/density.html)                               | ✅  | ✅  |
| [最大因果エントロピー逆強化学習（Maximum Causal Entropy IRL）](https://www.cs.cmu.edu/~bziebart/publications/maximum-causal-entropy.pdf) | [`algorithms.mce_irl`](https://imitation.readthedocs.io/en/latest/algorithms/mce_irl.html)                               | ✅  | ❌  |
| [敵対的逆強化学習（AIRL）](https://arxiv.org/abs/1710.11248)                                                                      | [`algorithms.airl`](https://imitation.readthedocs.io/en/latest/algorithms/airl.html)                                     | ✅  | ✅  |
| [生成的敵対的模倣学習（GAIL）](https://arxiv.org/abs/1606.03476)                                                                    | [`algorithms.gail`](https://imitation.readthedocs.io/en/latest/algorithms/gail.html)                                     | ✅  | ✅  |
| [人間の嗜好からの深層強化学習（Deep RL from Human Preferences）](https://arxiv.org/abs/1706.03741)                                      | [`algorithms.preference_comparisons`](https://imitation.readthedocs.io/en/latest/algorithms/preference_comparisons.html) | ✅  | ✅  |
| [Soft Q模倣学習（SQIL）](https://arxiv.org/abs/1905.11108)                                                                    | [`algorithms.sqil`](https://imitation.readthedocs.io/en/latest/algorithms/sqil.html)                                     | ✅  | ❌  |

ドキュメントは[こちらから確認できます](https://imitation.readthedocs.io/en/latest/)。

最新のベンチマーク結果は[こちら](https://imitation.readthedocs.io/en/latest/main-concepts/benchmark_summary.html)から閲覧できます。

## インストール

### 必要条件

* Python 3.8以上
* （任意）OpenGL（Gymnasium環境のレンダリング用）
* （任意）FFmpeg（レンダリング動画のエンコード用）

> 注：`imitation` は新しい [gymnasium](https://gymnasium.farama.org/) 環境APIのみをサポートしており、古い`gym` APIは対応していません。

### PyPIからのインストール

PyPIリリース版を使用するのが標準的で、ほとんどのユーザーに推奨されます。

```
pip install imitation
```

### ソースからのインストール

ソースコードからインストールする場合、次のコマンドを実行します。

```
git clone http://github.com/HumanCompatibleAI/imitation && cd imitation
pip install -e ".[dev]"
```

通常利用の場合：

```
pip install .
```

追加オプションとして、`tests`、`docs`、`parallel`、`atari`が利用可能です。

macOSユーザーは以下もインストールしてください。

```
brew install coreutils gnu-getopt parallel
```

## CLIクイックスタート

CLIスクリプトが提供されています。例えば、次のように使用します。

```bash
# PPOエージェントをpendulumで訓練し、エキスパートデモを収集
python -m imitation.scripts.train_rl with pendulum environment.fast policy_evaluation.fast rl.fast fast logging.log_dir=quickstart/rl/

# デモからGAILを訓練
python -m imitation.scripts.train_adversarial gail with pendulum environment.fast demonstrations.fast policy_evaluation.fast rl.fast fast demonstrations.path=quickstart/rl/rollouts/final.npz demonstrations.source=local

# デモからAIRLを訓練
python -m imitation.scripts.train_adversarial airl with pendulum environment.fast demonstrations.fast policy_evaluation.fast rl.fast fast demonstrations.path=quickstart/rl/rollouts/final.npz demonstrations.source=local
```

## Pythonインターフェースクイックスタート

例として[examples/quickstart.py](examples/quickstart.py)があります。

### 密度報酬ベースライン

密度ベースの報酬基準の例として[こちらのノートブック](docs/tutorials/7_train_density.ipynb)があります。

# 引用（BibTeX）

```
@misc{gleave2022imitation,
  author = {Gleave, Adam and Taufeeque, Mohammad and Rocamonde, Juan and Jenner, Erik and Wang, Steven H. and Toyer, Sam and Ernestus, Maximilian and Belrose, Nora and Emmons, Scott and Russell, Stuart},
  title = {imitation: Clean Imitation Learning Implementations},
  year = {2022},
  howPublished = {arXiv:2211.11972v1 [cs.LG]},
  archivePrefix = {arXiv},
  eprint = {2211.11972},
  primaryClass = {cs.LG},
  url = {https://arxiv.org/abs/2211.11972},
}
```

## 貢献

詳しくは[貢献方法](https://imitation.readthedocs.io/en/latest/development/contributing/index.html)を参照してください。
