#!/bin/bash

echo "=== Git .env Cleanup Script ==="
echo "This script will help you remove .env from Git history"
echo ""

# Check if .env exists in current commit
if git ls-tree HEAD | grep -q ".env"; then
    echo "⚠️  .env file found in current commit"
else
    echo "✅ .env file not in current commit (good!)"
fi

# Check if .env exists in history
if git log --all --full-history -- .env | head -1 | grep -q "commit"; then
    echo "⚠️  .env file found in Git history - needs cleanup"
    echo ""
    echo "Choose cleanup method:"
    echo "1. git filter-repo (recommended)"
    echo "2. git filter-branch (traditional)"
    echo ""
    echo "For option 1, run:"
    echo "pip install git-filter-repo"
    echo "git filter-repo --path .env --invert-paths"
    echo ""
    echo "For option 2, run:"
    echo "git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env' --prune-empty --tag-name-filter cat -- --all"
    echo ""
    echo "After cleanup, force push:"
    echo "git push origin --force --all"
    echo "git push origin --force --tags"
else
    echo "✅ .env file not found in Git history"
fi

echo ""
echo "🔑 IMPORTANT: Don't forget to rotate/invalidate any exposed API keys!"
echo ""
echo "After cleanup, create .env.example:"
echo "echo 'SERPER_API_KEY=your_serper_api_key_here' > .env.example"
echo "git add .env.example"
echo "git commit -m 'Add .env.example template'" 