# Development Workflow

## Branch Strategy

main
develop
feature/*

## Workflow

feature/*
↓
develop
↓
main

## Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
git push -u origin feature/my-feature

Merge To Develop
git checkout develop
git pull origin develop
git merge feature/my-feature
git push origin develop
