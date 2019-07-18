---
title: Linux-Mint-reset-panel
date: 2017-10-01 10:03:37
categories: Linux
tags:
    - Linux
---

here is the tutorial for resetting your panel menu in Linux Mint

<!-- more -->

so what you all have to do are :

1. Open up your terminal (ctrl+alt+t)

2. Run the following command in the terminal:
```
    gsettings reset-recursively org.cinnamon (THIS IS FOR CINNAMON)
    gsettings reset-recursively org.mate.panel (THIS IS FOR MATE)
```
3. Hit Enter
4. Taraa!!! you should have your panel back to their default again.

NOTE :

- you may login out and login in again to get them work again, in some cases you need to reboot your system.
- tested and worked on my MATE Dekstop Envir

ref:
[https://community.linuxmint.com/tutorial/view/2195](https://community.linuxmint.com/tutorial/view/2195)
