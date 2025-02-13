#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
import subprocess, re, sys, os

app = FastAPI()

API_KEY_FILE = "/etc/william/apiX"

# ======= Fungsi Utilitas =======
def check_ulimit():
    result = subprocess.run("ulimit -c", capture_output=True, text=True, shell=True, executable="/bin/bash")
    if result.returncode == 0 and result.stdout.strip() != "0":
        print("Im Watching You...")
        print("- @user_legend")
        sys.exit()

check_ulimit()

def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    return "please_input_your_apikey"

def save_api_key(api_key: str):
    try:
        with open(API_KEY_FILE, "w") as f:
            f.write(api_key)
        print(f"API key disimpan ke {API_KEY_FILE}")
    except Exception as e:
        print(f"Gagal menyimpan API key ke file: {e}")

api_key = load_api_key()
VALID_API_KEYS = {api_key: "admin"}

def check_api_key(x_api_key: str = Header(None)) -> str:
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

def remove_escape_codes(text: str) -> str:
    ansi_escape = re.compile(r'(\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]))')
    return ansi_escape.sub("", text)

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=False)
        filter_words = [
            "curl is already installed",
            "Wget is already installed",
            "Client Name Accepted",
            "IP Address Accepted",
            "Script Active !",
            "Checking..."
        ]
        cleaned_stdout = remove_escape_codes(result.stdout)
        filtered_stdout = "\n".join(
            line for line in cleaned_stdout.strip().split("\n") 
            if all(word not in line for word in filter_words)
        )      
        return {
            "stdout": filtered_stdout,
            "stderr": remove_escape_codes(result.stderr.strip()),
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

#======= SSH =======#
class SSHCreate(BaseModel):
    user: str
    password: str
    limit_quota: str
    exp: str
    limit_ip: str
class SSHTrial(BaseModel):
    exp: str
class SSHRenew(BaseModel):
    user: str
    exp: str
class SSHUnlocknLocknDel(BaseModel):
    user: str
#======= SSH =======#
#======= Endpoint SSH =======#
@app.post("/user_legend/add-ssh")
def add_ssh(request: SSHCreate, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-sshx', request.user, request.password, request.limit_quota, request.exp, request.limit_ip]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/trial-ssh")
def trial_ssh(request: SSHTrial, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[0-9]+$', request.exp):
        raise HTTPException(status_code=400, detail="Invalid username format. Only Numeric are allowed.")
    command = ['trial-sshx', request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-ssh")
def renew_ssh(request: SSHRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-sshx', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-ssh")
def delete_ssh(request: SSHUnlocknLocknDel, x_api_key: str = Depends(check_api_key)):
    command = ['del-sshx', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/lock-ssh")
def lock_ssh(request: SSHUnlocknLocknDel, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['lock-ssh', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/unlock-ssh")
def unlock_ssh(request: SSHUnlocknLocknDel, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['unlock-ssh', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/cek-ssh")
def cek_ssh(x_api_key: str = Depends(check_api_key)):
    command = ["cek"]
    return run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)
#======= Endpoint SSH =======#
#======= L2TP =======#
class L2TPCreate(BaseModel):
    user: str
    password: str
    exp: str
class L2TPRenew(BaseModel):
    user: str
    exp: str
class L2TPDelete(BaseModel):
    user: str
#======= L2TP =======#
#======= Endpoint L2TP =======#
@app.post("/user_legend/add-l2tp")
def add_l2tp(request: L2TPCreate, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-l2tpx', request.user, request.password, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-l2tp")
def renew_l2tp(request: L2TPRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-l2tpx', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-l2tp")
def del_l2tp(request: L2TPDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['del-l2tpx', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)
#======= Endpoint L2TP =======#
#======= XRAY WS =======#
class XRAYWSCreate(BaseModel):
    user: str
    exp: str
    limit_quota: str
    limit_ip: str
class XRAYWSTrial(BaseModel):
    exp: str
    limit_ip: str
class XRAYWSDelete(BaseModel):
    user: str
class XRAYWSRenew(BaseModel):
    user: str
    exp: str
class XRAYWSDetail(BaseModel):
    user: str
#======= XRAY WS =======#
#======= Endpoint XRAY WS =======#
@app.post("/user_legend/add-vmessws")
def add_vmessws(request: XRAYWSCreate, x_api_key: str = Depends(check_api_key)): 
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-vmws', request.user, request.exp, request.limit_quota, request.limit_ip]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/trial-vmessws")
def trial_vmessws(request: XRAYWSTrial, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[0-9]+$', request.exp):
        raise HTTPException(status_code=400, detail="Invalid username format. Only Numeric are allowed.")
    command = ['trial-vmws', request.exp, request.limit_ip]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-vmessws")
def del_vmessws(request: XRAYWSDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['del-vmws', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-vmessws")
def renew_vmessws(request: XRAYWSRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-vmws', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/detail-vmessws")
def detail_vmessws(request: XRAYWSDetail, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['detail-vmws', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/add-vlessws")
def add_vlessws(request: XRAYWSCreate, x_api_key: str = Depends(check_api_key)): 
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-vlws', request.user, request.exp, request.limit_quota, request.limit_ip]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/trial-vlessws")
def trial_vlessws(request: XRAYWSTrial, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[0-9]+$', request.exp):
        raise HTTPException(status_code=400, detail="Invalid username format. Only Numeric are allowed.")
    command = ['trial-vlws', request.exp, request.limit_ip]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-vlessws")
def del_vlessws(request: XRAYWSDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['del-vlws', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-vlessws")
def renew_vlessws(request: XRAYWSRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-vlws', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/detail-vlessws")
def detail_vlessws(request: XRAYWSDetail, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['detail-vlws', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/add-trojanws")
def add_trojanws(request: XRAYWSCreate, x_api_key: str = Depends(check_api_key)): 
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-trojanws', request.user, request.exp, request.limit_quota, request.limit_ip]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/trial-trojanws")
def trial_trojanws(request: XRAYWSTrial, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[0-9]+$', request.exp):
        raise HTTPException(status_code=400, detail="Invalid username format. Only Numeric are allowed.")
    command = ['trial-trojanws', request.exp, request.limit_ip]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-trojanws")
def del_trojanws(request: XRAYWSDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['del-trojanws', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-trojanws")
def renew_trojanws(request: XRAYWSRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-trojanws', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/detail-trojanws")
def detail_trojanws(request: XRAYWSDetail, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['detail-trojanws', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)
#======= Endpoint XRAY WS =======#
#======= XRAY GRPC =======#
class XRAYGRPCCreate(BaseModel):
    user: str
    exp: str
    limit_quota: str
class XRAYGRPCTrial(BaseModel):
    exp: str
class XRAYGRPCRenew(BaseModel):
    user: str
    exp: str
class XRAYGRPCDetailnDelete(BaseModel):
    user: str
#======= XRAY GRPC =======#
#======= Endpoint XRAY GRPC =======#
@app.post("/user_legend/add-vmessgrpc")
def add_vmessgrpc(request: XRAYGRPCCreate, x_api_key: str = Depends(check_api_key)): 
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-vmgrpc', request.user, request.exp, request.limit_quota]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/trial-vmessgrpc")
def trial_vmessgrpc(request: XRAYGRPCTrial, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[0-9]+$', request.exp):
        raise HTTPException(status_code=400, detail="Invalid username format. Only Numeric are allowed.")
    command = ['trial-vmgrpc', request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-vmessgrpc")
def del_vmessgrpc(request: XRAYGRPCDetailnDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['del-vmgrpc', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-vmessgrpc")
def renew_vmessgrpc(request: XRAYGRPCRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-vmgrpc', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/detail-vmessgrpc")
def detail_vmessgrpc(request: XRAYGRPCDetailnDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['detail-vmgrpc', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/add-vlessgrpc")
def add_vlessgrpc(request: XRAYGRPCCreate, x_api_key: str = Depends(check_api_key)): 
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-vlgrpc', request.user, request.exp, request.limit_quota]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/trial-vlessgrpc")
def trial_vlessgrpc(request: XRAYGRPCTrial, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[0-9]+$', request.exp):
        raise HTTPException(status_code=400, detail="Invalid username format. Only Numeric are allowed.")
    command = ['trial-vlgrpc', request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-vlessgrpc")
def del_vlessgrpc(request: XRAYGRPCDetailnDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['del-vlgrpc', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-vlessgrpc")
def renew_vlessgrpc(request: XRAYGRPCRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-vlgrpc', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/detail-vlessgrpc")
def detail_vlessgrpc(request: XRAYGRPCDetailnDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['detail-vlgrpc', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/add-trojangrpc")
def add_trojangrpc(request: XRAYGRPCCreate, x_api_key: str = Depends(check_api_key)): 
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['add-trojangrpc', request.user, request.exp, request.limit_quota]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/trial-trojangrpc")
def trial_trojangrpc(request: XRAYGRPCTrial, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[0-9]+$', request.exp):
        raise HTTPException(status_code=400, detail="Invalid username format. Only Numeric are allowed.")
    command = ['trial-trojangrpc', request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.delete("/user_legend/del-trojangrpc")
def del_trojangrpc(request: XRAYGRPCDetailnDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['del-trojangrpc', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/renew-trojangrpc")
def renew_trojangrpc(request: XRAYGRPCRenew, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['renew-trojangrpc', request.user, request.exp]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/detail-trojangrpc")
def detail_trojangrpc(request: XRAYGRPCDetailnDelete, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['detail-trojangrpc', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)
#======= Endpoint XRAY GRPC =======#
#======= XRAY TOOLS =======#
class XRAYTOOLSChangeUUID(BaseModel):
    uuidold: str
    uuidnew: str = ""

class XRAYTOOLSLocknUnlock(BaseModel):
    user: str
#======= XRAY TOOLS =======#
#======= Endpoint XRAY TOOLS =======#
@app.get("/user_legend/cek-xray")
def cek_xray(x_api_key: str = Depends(check_api_key)):
    command = ["cek-xray"]
    return run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.post("/user_legend/change-uuid")
def change_uuid(request: XRAYTOOLSChangeUUID, x_api_key: str = Depends(check_api_key)):
    command = ['change-uuidx', request.uuidold, request.uuidnew]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/lock-xray")
def lock_xray(request: XRAYTOOLSLocknUnlock, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['lock-xray', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)

@app.get("/user_legend/unlock-xray")
def unlock_xray(request: XRAYTOOLSLocknUnlock, x_api_key: str = Depends(check_api_key)):
    if not re.match(r'^[a-zA-Z0-9_]+$', request.user):
        raise HTTPException(status_code=400, detail="Invalid username format. Only alphanumeric and underscore are allowed.")
    command = ['unlock-xray', request.user]
    result = run_command(command)
    return result if result["returncode"] == 0 else HTTPException(status_code=500, detail=result)
#======= Endpoint XRAY TOOLS =======#

# ======= Menjalankan Server =======
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5069, workers=5)