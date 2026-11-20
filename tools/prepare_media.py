# -*- coding: utf-8 -*-
"""Build web-ready copies of the originals in Media/ into assets/.

Originals are never modified. Re-run after adding entries to the tables below:
    python tools/prepare_media.py
Needs: pip install Pillow imageio-ffmpeg
"""
import os
import subprocess
import sys

from PIL import Image, ImageOps
import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Media")
IMG_OUT = os.path.join(ROOT, "assets", "img")
VID_OUT = os.path.join(ROOT, "assets", "video")
FF = imageio_ffmpeg.get_ffmpeg_exe()
Image.MAX_IMAGE_PIXELS = None

SHOOT = "Others/2021-12-01_shooting-fsa_robotique_robotics_robot_pellois_charlier_b52_0729_s.seyen000%s.jpg"
PIM = "Others/PIM juin 2024/2024-06-21_shooting_fsa_presentations_projets_uliege_s.seyen_000%s.jpg"
SAWYER = "Outreach_blurred/Concours sawyer 16_03_2022_Robotix academy/"
AI4WORK = "Outreach/démo AI4work 26_05_2023/"
ROBOTIX = "Outreach/Roboitx academy annual meeting 18_11_2021/"

# source (relative to Media/) -> (output name, max width)
PHOTOS = {
    "General/DSC05315.JPG": ("sawyer-cable-1", 2400),
    "General/DSC05316.JPG": ("sawyer-cable-2", 1600),
    "General/pic2.JPG": ("sawyer-cable-3", 1600),
    "General/Picture_Louis_Dehaybe.png": ("portrait", 800),
    SHOOT % "48": ("kuka-draping-1", 1600),
    SHOOT % "50": ("kuka-draping-2", 1600),
    SHOOT % "55": ("kuka-draping-3", 1200),
    SHOOT % "56": ("kuka-draping-4", 1600),
    PIM % "71": ("student-projects-1", 1600),
    PIM % "75": ("student-projects-2", 1600),
    SAWYER + "20220316_132808.jpg": ("sawyer-competition-1", 1600),
    SAWYER + "20220316_152631.jpg": ("sawyer-competition-2", 1600),
    SAWYER + "262706074_870480186952794_7388050668464424372_n.jpg": ("sawyer-competition-3", 1600),
    SAWYER + "ConcoursSawyer3.jpg": ("sawyer-competition-4", 1600),
    AI4WORK + "IMG_2046.JPG": ("ai4work-1", 1600),
    AI4WORK + "IMG_2052.JPG": ("ai4work-2", 1600),
    AI4WORK + "IMG_2055.JPG": ("ai4work-3", 1600),
    AI4WORK + "IMG_2066.JPG": ("ai4work-4", 1600),
    "Outreach_blurred/Printemps des sciences 21_03_2022/PrintempsSciences2.jpg": ("printemps-sciences", 1600),
    ROBOTIX + "DSC_0148.JPG": ("robotix-2021-1", 1600),
    ROBOTIX + "IMG_6401.JPG": ("robotix-2021-2", 1600),
    ROBOTIX + "IMG_6405.JPG": ("robotix-2021-3", 1600),
    "Projects/AACOMA/Roadshow ACCOMA Liège/IMG_6251.jpg": ("aacoma-roadshow-1", 1600),
    "Projects/AACOMA/Roadshow ACCOMA Liège/IMG_6261.jpg": ("aacoma-roadshow-2", 1600),
    "Projects/AACOMA/Training module/IMG_6250.jpg": ("aacoma-training", 1600),
    "Projects/AACOMA/cap1.png": ("aacoma-cell-1", 1600),
    "Projects/AACOMA/cap2.png": ("aacoma-cell-2", 1600),
    "Research/ICRA2022 workshop/IMG_20220524_151914.jpg": ("icra-2022", 1400),
    "Research/IMSD/1782439237922.jfif": ("imsd-2026-1", 1600),
    "Research/IMSD/1782439238325.jfif": ("imsd-2026-2", 1600),
    "Research/scene_8_PBS_35_trial_2_part1.png": ("servoing-trajectories", 1600),
    "Research/SE3drawing.png": ("se3-setup", 1400),
    "Research/shape_servoing_mujoco_simu2.png": ("servoing-shell-mujoco", 1600),
}

# diagrams and plots: kept sharp as WebP
FIGURES = {
    "Research/cable_3D_2.png": "cable-3d",
    "Research/results1.png": "results-pbs",
    "Research/results2.png": "results-se3",
    "Research/results3.png": "results-success",
    "Research/results4.png": "results-error",
    "Research/shape_servoing_real.png": "servoing-real-frame",
    "Research/shape_servoing_mujoco_simu.png": "servoing-cable-mujoco",
    "Research/ICRA2022 workshop/experiment 1.png": "icra-experiment",
    "Research/ICRA2022 workshop/subfig.png": "icra-subfig",
    "Research/IMSD/Picture1.png": "servo-constraints-cases",
    "Projects/AACOMA/Roadshow3/grippers.png": "aacoma-grippers",
    "Projects/AACOMA/Roadshow3/system.png": "aacoma-system",
    "Projects/AACOMA/Roadshow3/steps.png": "aacoma-steps",
    "Projects/AACOMA/Roadshow3/method.png": "aacoma-method",
    "Projects/AACOMA/communication.png": "aacoma-communication",
    "Projects/AACOMA/AACOMA_logo.png": "aacoma-logo",
    "Projects/Intelligent robotics/Picture1.png": "slam-path-following",
    "Projects/Project microcontroller/Capture d'écran 2026-11-14 141810.png": "stabilizer-timer",
    "Projects/Project microcontroller/Capture d'écran 2026-11-14 142025.png": "stabilizer-wiring",
    "Projects/Project microcontroller/Picture1.png": "stabilizer-principle",
    "Projects/Projet trans Gramme/Picture1.png": "nesting-scan",
    "Projects/Projet trans Gramme/Picture2.png": "nesting-layout-1",
    "Projects/Projet trans Gramme/Picture3.png": "nesting-layout-2",
    "Projects/Projet trans Gramme/Picture4..png": "nesting-result",
}

# source -> (output name, max width, speed factor)
VIDEOS = {
    "Research/shape_servoing_cable_real.mp4": ("servoing-cable-real", 1280, 1),
    "Research/results.mp4": ("servoing-comparison", 1280, 1),
    "Research/shape_servoing_cable_simu.mp4": ("servoing-cable-sim", 1072, 1),
    "Research/shape_servoing_shell_simu.mp4": ("servoing-shell-sim-1", 1088, 1),
    "Research/shape_servoing_shell_simu2.mp4": ("servoing-shell-sim-2", 1088, 1),
    "Research/shape_servoing_shell_simu3.mp4": ("servoing-shell-sim-3", 1088, 1),
    "Research/ICRA2022 workshop/Media1.mp4": ("icra-sim-1", 1280, 1),
    "Research/ICRA2022 workshop/Media2.mp4": ("icra-sim-2", 1280, 1),
    "Research/IMSD/Media1.mp4": ("servo-constraints-1", 900, 1),
    "Research/IMSD/Media2.mp4": ("servo-constraints-2", 900, 1),
    "Research/IMSD/Media3.mp4": ("servo-constraints-3", 900, 1),
    "Research/IMSD/Media4.mp4": ("servo-constraints-4", 900, 1),
    "Research/IMSD/Media5.mp4": ("servo-constraints-5", 900, 1),
    "Research/IMSD/Media6.mp4": ("servo-constraints-6", 900, 1),
    "Projects/AACOMA/Media1_compressed.mp4": ("aacoma-draping", 1280, 1),
    "Projects/AACOMA/Roadshow5/draping édité.mp4": ("aacoma-draping-2", 1280, 1),
    "Projects/AACOMA/hand_draping.mp4": ("aacoma-demonstration", 1280, 1),
    "Projects/Intelligent robotics/Dehaybe _ Schneider.mp4": ("slam-youbot", 1280, 8),
}


def src(rel):
    return os.path.join(SRC, *rel.split("/"))


def stale(s, d):
    return not os.path.exists(d) or os.path.getmtime(d) < os.path.getmtime(s)


def load(path):
    im = ImageOps.exif_transpose(Image.open(path))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
    return im


def photos():
    for rel, (name, width) in PHOTOS.items():
        s, d = src(rel), os.path.join(IMG_OUT, name + ".jpg")
        if not stale(s, d):
            continue
        im = load(s)
        if im.mode == "RGBA":
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        im = im.convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(d, quality=82, optimize=True, progressive=True)
        print("photo ", name, im.size, os.path.getsize(d) // 1024, "KB")


def figures():
    for rel, name in FIGURES.items():
        s, d = src(rel), os.path.join(IMG_OUT, name + ".webp")
        if not stale(s, d):
            continue
        im = load(s)
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(d, quality=88, method=6)
        print("figure", name, im.size, os.path.getsize(d) // 1024, "KB")


def videos():
    for rel, (name, width, speed) in VIDEOS.items():
        s = src(rel)
        d = os.path.join(VID_OUT, name + ".mp4")
        poster = os.path.join(VID_OUT, name + ".jpg")
        if not stale(s, d):
            continue
        vf = "scale='min(%d,iw)':-2:flags=lanczos" % width
        if speed != 1:
            vf = "setpts=PTS/%d," % speed + vf
        cmd = [FF, "-y", "-loglevel", "error", "-i", s, "-an", "-vf", vf, "-r", "30",
               "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", d]
        subprocess.run(cmd, check=True)
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", "1", "-i", d, "-frames:v", "1",
                        "-q:v", "4", poster], check=True)
        print("video ", name, os.path.getsize(d) // 1024, "KB")


if __name__ == "__main__":
    os.makedirs(IMG_OUT, exist_ok=True)
    os.makedirs(VID_OUT, exist_ok=True)
    missing = [r for r in list(PHOTOS) + list(FIGURES) + list(VIDEOS) if not os.path.exists(src(r))]
    if missing:
        sys.exit("Missing source files:\n  " + "\n  ".join(missing))
    photos()
    figures()
    videos()
    print("done")
