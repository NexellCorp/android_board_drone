"""Emit commands needed for nexell pyrope specific OTA update """

import common


def FullOTA_InstallEnd(info):
    try:
        boot_img = info.output_zip.read("boot.img")
    except KeyError:
        print "no boot.img in target_files, skipping install"
    else:
        WriteBootImage(info, boot_img)

    try:
        bootloader_img = info.input_zip.read("RADIO/bootloader")
    except KeyError:
        print "no bootloader in target_files, skipping install"
    else:
        WriteBootloader(info, bootloader_img, "spirom")

    try:
        secondboot_img = info.input_zip.read("RADIO/2ndbootloader")
    except KeyError:
        print "no 2ndbootloader in target_files, skipping install"
    else:
        WriteSecondBootloader(info, secondboot_img, "spirom")


def IncrementalOTA_IntallEnd(info):
    try:
        target_boot_img = info.target_zip.read("boot.img")
        try:
            source_boot_img = info.source_zip.read("boot.img")
        except KeyError:
            source_boot_img = None

        if source_boot_img == target_boot_img:
            print "boot.img unchanged, skipping"
        else:
            WriteBootImage(info, target_boot_img)
    except KeyError:
        print "no boot.img in target_files, skipping install"


def WriteBootImage(info, boot_img):
    print "WriteBootImage ..."
    info.script.Print("Writing boot image...")
    fstab = info.script.info["fstab"]
    if fstab:
        p = fstab["/boot"]
        info.script.AppendExtra('nexell.pyrope.write_boot_image(package_extract_file("boot.img"), "%s");' % p.device)
    else:
        print "can't find fstab, do nothing"


def WriteBootloader(info, bootloader_img, boot_type):
    print "WriteBootloader ..."
    common.ZipWriteStr(info.output_zip, "bootloader", bootloader_img)
    info.script.Print("Writing bootloader ...")
    info.script.AppendExtra('nexell.pyrope.write_bootloader(package_extract_file("bootloader"), "%s");' % boot_type)


def WriteSecondBootloader(info, secondbootloader_img, boot_type):
    print "WriteSecondBootloader ..."
    common.ZipWriteStr(info.output_zip, "2ndbootloader", secondbootloader_img)
    info.script.Print("Writing secondbootloader ...")
    info.script.AppendExtra('nexell.pyrope.write_secondbootloader(package_extract_file("2ndbootloader"), "%s");' % boot_type)
