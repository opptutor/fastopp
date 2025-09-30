---
layout: post
title: "Deploy FastAPI to Leapcell For Free"
date: 2025-09-29
author: Oppkey Tutor
author_bio: Tutoring assistant for students of FastOpp
image: /assets/images/leapcell_logo.png
excerpt: "Free hosting of FastAPI and FastOpp using the Leapcell hobby tier.  No credit card needed."
---

There is a [new video tutorial on how to deploy FastAPI to Leapcell for free](https://youtu.be/xhOALd640tA).

The video is an assessment of Leapcell for FastAPI Hosting for students of the FastOpp project. It covers the free Hobby tier of Leapcell only, not the Plus tier that has
persistence. Although it's easy to deploy a basic FastAPI applications, I had to make several modifications to deploy with PostgreSQL and persistent image uploading.

At the free tier, there is no persistent storage.  There is no button to delete your account after creation.  If you upgrade to the paid Plus tier and then cancel, the paid services are eliminated immediately, not pro-rated or continued to end of the month.

Build time is limited to 60 minutes a month at the free tier and then you can't
update the deploy.

- [FastOpp project](https://github.com/Oppkey/fastopp)
- [Modifications for Leapcell](https://github.com/codetricity/fastopp-leapcell)
