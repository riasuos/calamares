#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import libcalamares
import subprocess
from libcalamares.utils import check_target_env_call, target_env_call


class PackageManager:

    """ Package manager class.

    :param backend:
    """

    def __init__(self, backend):
        self.backend = backend

    def install(self, pkgs, from_local=False):
        """ Installs packages.

        :param pkgs:
        :param from_local:
        """

        if self.backend == "pacman":
            if from_local:
                pacman_flags = "-U"
            else:
                pacman_flags = "-Sy"

            check_target_env_call(["pacman", pacman_flags, "--noconfirm"
                                  ] + pkgs)

    def remove(self, pkgs):
        """ Removes packages.

        :param pkgs:
        """

        if self.backend == "pacman":
            check_target_env_call(["pacman", "-Rs", "--noconfirm"]
                                  + pkgs)

    def upgrade(self):
        """ upgrades all packages.

        """

        if self.backend == "pacman":
            try:
                check_target_env_call(["pacman", "-Syyu", "--noconfirm"])
            except:
                print("unresolvable package conflicts detected")


def get_language():
    output = libcalamares.globalstorage.value("localeConf")
    lang = output["LANG"]

    parts = lang.split(".")
    if len(parts) < 1:
        return ""

    lang = parts[0].lower()
    lang = lang.replace("_", "-")
    return lang


virtualbox = False #global var for virtualbox_check

def virtualbox_check():
    command = "dmidecode -s system-product-name"
    output = subprocess.check_output(['sh','-c', command]).decode('ascii')
    substring = output[0:10].lower()

    global virtualbox
    if substring == "virtualbox":
        virtualbox = True
    else:
        virtualbox = False

    return virtualbox

def packagelist_filter(pkgs, pkg_remove_filter, first_index, last_index):
    new_package_list = []
    for pkg in pkgs:
        part = pkg[first_index:last_index].lower()
        if part != pkg_remove_filter:
            new_package_list.append(pkg)

    return new_package_list


def run_operations(pkgman, entry):
    """ Call package manager with given parameters.

    :param pkgman:
    :param entry:
    """

    for key in entry.keys():
        if key == "install":
            pkgman.install(entry[key])
        elif key == "remove":
            if virtualbox:
                pkgman.remove(packagelist_filter(entry[key], "virtualbox", 0, 10))
            else:
                pkgman.remove(entry[key])
        elif key == "localInstall":
            pkgman.install(entry[key], from_local=True)


def run():
    """ Calls routine with detected package manager to install locale packages
    or remove drivers not needed on the installed system.

    :return:
    """

    virtualbox_check()

    backend = libcalamares.job.configuration.get("backend")

    if backend not in ("pacman"):
        return "Bad backend", "backend=\"{}\"".format(backend)

    pkgman = PackageManager(backend)
    operations = libcalamares.job.configuration.get("operations", [])

    for entry in operations:
        run_operations(pkgman, entry)

    if libcalamares.globalstorage.contains("packageOperations"):
        run_operations(pkgman,
                       libcalamares.globalstorage.value("packageOperations"
                       ))

    return None
