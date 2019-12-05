#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import libcalamares.utils


def run():
    """ Calls routine to create kernel initramfs image.
    :return:
    """
    try:
      # Fixing Permission
        libcalamares.utils.check_target_env_call(["chown", "root:root", "/"])
        libcalamares.utils.check_target_env_call(["chmod", "755", "/"])
    except Exception as e:
        print(e)  # printing exception

    return None
