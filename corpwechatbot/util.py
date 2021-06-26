#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: util.py
            Description:
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://blog.gentlecp.com
            Create Date: 2021/4/7 
-----------------End-----------------------------
"""

from pathlib import Path
from hashlib import sha1


def is_image(image_path: str):
    p_image = Path(image_path)
    if not p_image.is_file():
        return False
    if p_image.suffix != '.jpg' and p_image.suffix != '.png':
        return False
    if p_image.stat().st_size > 2 * 1024 * 1024 or p_image.stat().st_size <= 5:
        # image no more than 2M
        return False
    return True


def is_voice(voice_path: str):
    p_voice = Path(voice_path)
    if not p_voice.is_file():
        return False
    if p_voice.suffix != '.amr':
        return False
    if p_voice.stat().st_size > 2 * 1024 * 1024 or p_voice.stat().st_size <= 5:
        # voice no more than 2M
        return False
    return True


def is_video(video_path: str):
    p_video = Path(video_path)
    if not p_video.is_file():
        return False
    if p_video.suffix != '.mp4':
        return False
    if p_video.stat().st_size > 10 * 1024 * 1024 or p_video.stat().st_size <= 5:
        # video no more than 10M
        return False
    return True


def is_file(file_path: str):
    p_file = Path(file_path)
    if not p_file.is_file():
        return False
    if p_file.stat().st_size > 20 * 1024 * 1024 or p_file.stat().st_size <= 5:
        # file no more than 2M
        return False
    return True

def cal_signature(token, timestamp, nonce, msg_encrypt):
    return

