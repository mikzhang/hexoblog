---
title: Git_clone某个分支
date: 2017-07-28 11:48:07
categories: Git
tags:
     - Git
---

<!-- more -->

## clone 某个分支：
git clone -b srcbr git://github.com/xxx/xxx.git

## clone所有分支
git clone git://github.com/xxx/xxx.git

## List or delete (if used with -d) the remote-tracking branches.
```
git branch -r           
* master
  origin/HEAD -> origin/master
  origin/master
  origin/b1
```

## Switch branches or restore working tree files.
git checkout b1
