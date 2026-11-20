#!/usr/bin/env bash
# Build a small fake research repo to try whychanged on.
# Usage: bash demo/make_demo_repo.sh /tmp/demo-lab
set -euo pipefail
DEST="${1:-./demo-lab}"
rm -rf "$DEST" && mkdir -p "$DEST/configs" && cd "$DEST"
git init -q -b main
git config user.name "Alice" && git config user.email "alice@example.com"

cat > configs/train.yaml <<'EOF'
train:
  lr: 0.001
  batch_size: 32
  dropout: 0.1
  epochs: 20
EOF
cat > .env.example <<'EOF'
CUDA_VISIBLE_DEVICES=0
DATA_DIR=/data/protein/v1
EOF
git add . && git commit -qm "initial training setup"

# A works on a branch: one change with a reason, one without
git checkout -qb feat/head-dropout
sed -i.bak 's/dropout: 0.1/dropout: 0.3/; s/batch_size: 32/batch_size: 64/' configs/train.yaml && rm configs/train.yaml.bak
git commit -qam "raise dropout, val loss went up after epoch 5, overfitting"

# An older branch that someone ran weeks ago
git checkout -q main
git checkout -qb exp/old-lr
sed -i.bak 's/lr: 0.001/lr: 0.0005/' configs/train.yaml && rm configs/train.yaml.bak
sed -i.bak 's#/data/protein/v1#/data/protein/v2#' .env.example && rm .env.example.bak
git commit -qam "lower lr to 5e-4, loss was unstable in the first 2 epochs"
git checkout -q feat/head-dropout

echo "Demo repo ready at $DEST (on branch feat/head-dropout)"
