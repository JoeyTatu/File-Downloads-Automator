from os import scandir, rename, makedirs
from os.path import splitext, exists, join
from shutil import move
from time import sleep

# import string
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "C:\\Users\\Joey\\Downloads"

base_dir = "C:\\Users\\Joey\\Desktop\\Sorted Downloads\\"
dest_dir_image = base_dir + "Images"
dest_dir_video = base_dir + "Videos"
dest_dir_audio = base_dir + "Audio"
dest_dir_documents = base_dir + "Documents"
dest_dir_installation = base_dir + "Installtions"
dest_dir_compressed = base_dir + "Compressed"
dest_dir_other = base_dir + "Other"

image_extensions = [
    '.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg',
    '.png', '.psd', '.svg', '.tiff', '.webp', '.jfif',
    '.jpe', '.jif', '.jfi', '.jp2', '.jpx', '.j2k',
    '.j2c', '.pdf', '.raw', '.indd', '.eps', '.tga',
    '.exr', '.hdr', '.bat', '.bpg', '.cgm', '.dcm',
    '.dpx', '.fits', '.flif', '.fpx', '.gif', '.hdri',
    '.ico', '.ipl', '.j2c', '.jng', '.jp2', '.jpc',
    '.jpe', '.jpeg', '.jpf', '.jpg', '.jpm', '.jpx',
    '.jxr', '.j2k', '.j3d', '.pdf', '.pict', '.png',
    '.pnm', '.pns', '.ps', '.ps2', '.ps3', '.psd',
    '.svg', '.svgz', '.t38', '.tga', '.tiff', '.tif',
    '.uyvy', '.vicar', '.viff', '.wbmp', '.wdp', '.webp',
    '.xbm', '.xpm', '.xwd', '.yuv'
]

video_extensions = [
    '.3g2', '.3gp', '.asf', '.avi', '.flv', '.mkv',
    '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf',
    '.vob', '.wmv', '.webm', '.m4v', '.ogv', '.ogm',
    '.m2v', '.ts', '.mxf', '.mp3', '.wav', '.aac',
    '.flac', '.wma', '.ogg', '.m4a', '.opus', '.mk3d',
    '.flv', '.m4v', '.webm', '.vob', '.avi', '.mov',
    '.mkv', '.mp4', '.mpg', '.mpeg', '.wmv', '.m2v',
    '.mxf', '.ogv', '.ogm', '.ts', '.mpg', '.mpeg',
    '.m2ts', '.webm', '.mk3d', '.avi', '.mov', '.mp4',
    '.mkv', '.3gp', '.flv', '.wmv', '.mpg', '.mpeg',
    '.m4v', '.ogg', '.ogv', '.m2v', '.ts', '.mxf',
    '.webm', '.mov', '.mp4', '.mkv', '.avi', '.wmv',
    '.flv', '.mpeg', '.mpg', '.m2v', '.m4v', '.webm',
    '.ogv', '.ogm', '.ts', '.mxf', '.mk3d'
]

audio_extensions = [
    '.mp3', '.wav', '.aac', '.flac', '.wma', '.ogg',
    '.m4a', '.opus', '.ac3', '.amr', '.ape', '.caf',
    '.dts', '.gsm', '.mka', '.mlp', '.mpc', '.ra',
    '.tta', '.wv', '.mp2', '.mp1', '.m3u', '.m4b',
    '.m4p', '.pls', '.ram', '.spx', '.vox', '.xspf',
    '.3ga', '.aa', '.aax', '.act', '.aiff', '.au',
    '.awb', '.dct', '.dss', '.dvf', '.g722', '.m2a',
    '.m4r', '.mid', '.mod', '.mpc', '.msv', '.oga',
    '.omg', '.opus', '.ra', '.raw', '.sln', '.tak',
    '.tta', '.vox', '.wav', '.wma', '.wv', '.8svx',
    '.cda', '.gsm', '.iff', '.kar', '.m3u', '.m4a',
    '.mid', '.mpa', '.mp3', '.mp4', '.oga', '.ogg',
    '.ra', '.rm', '.spx', '.voc', '.w64', '.wav',
    '.webm', '.xm'
]

document_extensions = [
    '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.odt', '.ods', '.odp', '.odg', '.odf', '.rtf',
    '.txt', '.pdf', '.html', '.htm', '.md', '.csv',
    '.tex', '.djvu', '.epub', '.fb2', '.mobi', '.chm',
    '.xps', '.ps', '.pptm', '.ppsx', '.ppsm', '.potx',
    '.potm', '.ppam', '.ppa', '.xlsm', '.xlsb', '.xltx',
    '.xltm', '.dotx', '.dotm', '.docm', '.dot', '.rtf',
    '.msg', '.eml', '.mht', '.mhtml', '.xml', '.wps',
    '.wpd', '.key', '.numbers', '.pages', '.indd', '.p65',
    '.cdx', '.cgm', '.cmx', '.djv', '.dxf', '.dwg',
    '.eps', '.pct', '.pict', '.psd', '.ai', '.cdr',
    '.wp', '.wp4', '.wp5', '.wp6', '.wpd', '.wpg'
]

installation_extensions = [
    '.exe', '.msi', '.deb', '.rpm', '.dmg', '.pkg', '.app',
    '.bat', '.sh', '.run', '.jar', '.com', '.gadget', '.wsf',
    '.cab', '.apk', '.xap', '.vb', '.vbs', '.vbe', '.ps1',
    '.psm1', '.psc1', '.scr', '.hta', '.cpl', '.reg', '.msp',
    '.mst', '.cmd', '.appx', '.appxbundle', '.xll', '.dll',
    '.ocx', '.sys', '.drv', '.efi', '.swf', '.air', '.rpm',
    '.deb', '.iso', '.img', '.toast', '.vcd', '.nrg', '.mdf',
    '.bin', '.cue', '.daa', '.ui', '.uxtheme', '.theme',
    '.deskthemepack', '.themepack'
]

compressed_extensions = [
    '.zip', '.7z', '.rar', '.tar', '.gz', '.bz2',
    '.xz', '.z', '.iso', '.img', '.nrg', '.mdf',
    '.bin', '.cue', '.daa', '.arc', '.arj', '.cab',
    '.tar.gz', '.tar.bz2', '.tar.xz', '.tar.z',
    '.tar.lz', '.tar.lzma', '.tar.sz', '.tar.lz4',
    '.tar.gz2', '.tar.z2', '.tar.zst', '.tar.zstd'
]

all_extensions = (
    image_extensions +
    video_extensions +
    audio_extensions +
    document_extensions +
    installation_extensions +
    compressed_extensions
)

# unique_extensions = list(set(all_extensions))
# all_possible_extensions = ['.' + char for char in string.ascii_lowercase]
# other_extensions = [ext for ext in all_possible_extensions if ext not in unique_extensions]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(F"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


def ensure_directory_exists(directory):
    if not exists(directory):
        makedirs(directory)


def move_file(dest, entry, name):
    ensure_directory_exists(dest)  # Ensure the destination folder exists

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            if exists(entry.path):  # Check if the file still exists
                if exists(join(dest, name)):
                    unique_name = make_unique(dest, name)
                    old_name = join(dest, name)
                    new_name = join(dest, unique_name)
                    rename(old_name, new_name)

                move(entry.path, dest)
                break  # Break out of the loop if the move is successful
        except PermissionError:
            logging.warning(
                f"PermissionError: File {name} is in use and cannot be moved.")
        except FileNotFoundError:
            logging.warning(
                f"FileNotFoundError: File {name} not found during move.")

        sleep(2 ** attempt)  # Exponential backoff: 2^attempt seconds delay

    else:
        logging.error(
            f"Failed to move file {name} after {max_retries} attempts.")


class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    # ? .upper is for not missing out on files with uppercase extensions
    def on_modified(self, event):
        if event.is_directory:
            return

        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_image_files(entry, name)
                self.check_video_files(entry, name)
                self.check_audio_files(entry, name)
                self.check_document_files(entry, name)
                self.check_installation_files(entry, name)
                self.check_compressed_files(entry, name)
                self.check_other_files(entry, name)

    def check_image_files(self, entry, name):
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_video_files(self, entry, name):
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_audio_files(self, entry, name):
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                move_file(dest_dir_audio, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_document_files(self, entry, name):
        for document_extension in document_extensions:
            if name.endswith(document_extension) or name.endswith(document_extension.upper()):
                move_file(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")

    def check_installation_files(self, entry, name):
        for installation_extension in installation_extensions:
            if name.endswith(installation_extension) or name.endswith(installation_extension.upper()):
                move_file(dest_dir_installation, entry, name)
                logging.info(f"Moved installation file: {name}")

    def check_compressed_files(self, entry, name):
        for compressed_extension in compressed_extensions:
            if name.endswith(compressed_extension) or name.endswith(compressed_extension.upper()):
                move_file(dest_dir_compressed, entry, name)
                logging.info(f"Moved compressed file: {name}")

    def check_other_files(self, entry, name):
        for ext in all_extensions:
            if name.endswith(ext) or name.endswith(ext.upper()):
                # File has a known extension, do not move
                return

        # If the loop completes without returning, move the file
        move_file(dest_dir_other, entry, name)
        logging.info(f"Moved other file: {name}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
