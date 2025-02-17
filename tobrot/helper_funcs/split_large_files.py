#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Akshay C | Shrimadhav U K | YK | 5MysterySD | Other Contributors 
#
# Copyright 2022 - TeamTele-LeechX
# 
# This is Part of < https://github.com/5MysterySD/Tele-LeechX >
# All Right Reserved

import asyncio
import os
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from tobrot import LOGGER, SP_LIT_ALGO_RITH_M


async def split_large_files(input_file, MAX_TG_SPLIT_FILE_SIZE):
    working_directory = os.path.dirname(os.path.abspath(input_file))
    new_working_directory = os.path.join(working_directory, str(time.time()))

    if not os.path.isdir(new_working_directory):
        os.makedirs(new_working_directory)
    VIDEO_SUFFIXES = ("MKV", "MP4", "MOV", "WMV", "3GP", "MPG", "WEBM", "AVI", "FLV", "M4V", "GIF")
    if input_file.upper().endswith(VIDEO_SUFFIXES):

        metadata = extractMetadata(createParser(input_file))
        total_duration = 0
        if metadata.has("duration"):
            total_duration = metadata.get("duration").seconds

        total_file_size = os.path.getsize(input_file)
        LOGGER.info(total_file_size)
        minimum_duration = (total_duration / total_file_size) * (MAX_TG_SPLIT_FILE_SIZE)
        minimum_duration = int(minimum_duration)

        start_time = 0
        end_time = minimum_duration
        base_name = os.path.basename(input_file)
        input_extension = base_name.split(".")[-1]

        i = 0
        flag = False

        while end_time <= total_duration:
            parted_file_name = f"{base_name}_part{str(i).zfill(5)}.{input_extension}"
            output_file = os.path.join(new_working_directory, parted_file_name)
            LOGGER.info(output_file)
            LOGGER.info(
                await cult_small_video(
                    input_file, output_file, str(start_time), str(end_time)
                )
            )
            LOGGER.info(f"Start time {start_time}, End time {end_time}, Itr {i}")

            start_time = end_time - 3
            end_time = end_time + minimum_duration
            i = i + 1

            if (end_time > total_duration) and not flag:
                end_time = total_duration
                flag = True
            elif flag:
                break

    elif SP_LIT_ALGO_RITH_M.lower() == "hjs":
        o_d_t = os.path.join(new_working_directory, os.path.basename(input_file))
        o_d_t = o_d_t + "."
        file_genertor_command = [
            "split",
            "--numeric-suffixes=1",
            "--suffix-length=5",
            f"--bytes={MAX_TG_SPLIT_FILE_SIZE}",
            input_file,
            o_d_t,
        ]
        await run_comman_d(file_genertor_command)

    elif SP_LIT_ALGO_RITH_M.lower() == "rar":
        o_d_t = os.path.join(
            new_working_directory,
            os.path.basename(input_file),
        )
        LOGGER.info(o_d_t)
        file_genertor_command = [
            "rar",
            "a",
            f"-v{MAX_TG_SPLIT_FILE_SIZE}b",
            "-m0",
            o_d_t,
            input_file,
        ]
        await run_comman_d(file_genertor_command)
    try:
        os.remove(input_file)
    except Exception as r:
        LOGGER.error(r)
    return new_working_directory


async def cult_small_video(video_file, out_put_file_name, start_time, end_time):
    file_genertor_command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", video_file, "-ss", start_time, "-to", end_time, "-async", "1", "-strict", "-2", "-map", "0:v", "-map", "0:a", "-map", "0:s?", "-c", "copy", "-map_chapters", "-1", out_put_file_name]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    LOGGER.info(t_response)
    return out_put_file_name


async def run_comman_d(command_list):
    process = await asyncio.create_subprocess_exec(
        *command_list,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return t_response, e_response
