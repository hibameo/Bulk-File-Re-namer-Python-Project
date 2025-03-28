import os
import shutil
import streamlit as st

def rename_files(folder_path, prefix="", suffix="", replace_text=None, new_text=None, numbering=False, extension=None):
    if not os.path.isdir(folder_path):
        return "Invalid folder path.", []

    files = sorted(os.listdir(folder_path))
    original_names = []
    new_names = []

    for index, filename in enumerate(files, start=1):
        old_path = os.path.join(folder_path, filename)
        if not os.path.isfile(old_path):
            continue
        
        name, ext = os.path.splitext(filename)
        
        if replace_text and new_text:
            name = name.replace(replace_text, new_text)
        
        if extension:
            ext = extension
        
        new_name = f"{prefix}{name}{suffix}{ext}"
        
        if numbering:
            new_name = f"{prefix}{str(index).zfill(3)}_{name}{suffix}{ext}"
        
        new_path = os.path.join(folder_path, new_name)
        
        if old_path != new_path:
            shutil.move(old_path, new_path)
            original_names.append(old_path)
            new_names.append(new_path)

    return "Renaming completed successfully!", new_names

def undo_rename(original_names, new_names):
    for old, new in zip(original_names, new_names):
        shutil.move(new, old)
    return "Undo completed successfully!"

st.title("Bulk File Renamer")
folder = st.text_input("Enter the folder path:")
prefix = st.text_input("Enter prefix:")
suffix = st.text_input("Enter suffix:")
replace_text = st.text_input("Text to replace:") or None
new_text = st.text_input("New text:") or None
numbering = st.checkbox("Enable numbering")
extension = st.text_input("New extension (e.g., .txt, .jpg):")
extension = f".{extension}" if extension else None

if st.button("Rename Files"):
    message, new_files = rename_files(folder, prefix, suffix, replace_text, new_text, numbering, extension)
    st.success(message)
    if new_files:
        st.write("New filenames:")
        st.write(new_files)

if st.button("Undo Renaming"):
    message = undo_rename(original_names, new_files)
    st.success(message)
