

# ========================= PKILL ENDPOINTS =========================

@app.post("/system/pkill/{process_name}")
async def pkill_process(process_name: str):
    """Kill processes by name using pkill"""
    try:
        result = subprocess.run(['pkill', '-f', process_name], 
                              capture_output=True, text=True, timeout=10)
        pids_result = subprocess.run(['pgrep', '-f', process_name], 
                                   capture_output=True, text=True)
        killed_pids = []
        if pids_result.stdout:
            killed_pids = pids_result.stdout.strip().split('\n')
        return {
            "status": "success" if result.returncode == 0 else "no_match",
            "process_name": process_name,
            "killed_pids": killed_pids,
            "command": f"pkill -f {process_name}",
            "return_code": result.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/system/killall/{process_name}")
async def killall_process(process_name: str):
    """Kill all processes with exact name match"""
    try:
        result = subprocess.run(['killall', process_name], 
                              capture_output=True, text=True, timeout=10)
        return {
            "status": "success" if result.returncode == 0 else "failed",
            "process_name": process_name,
            "command": f"killall {process_name}",
            "return_code": result.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/system/kill/{pid}")
async def kill_process_by_pid(pid: int):
    """Kill process by PID"""
    try:
        import os, signal
        os.kill(pid, signal.SIGTERM)
        return {"status": "success", "pid": pid}
    except ProcessLookupError:
        raise HTTPException(status_code=404, detail=f"Process {pid} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/system/processes")
async def list_processes():
    """List processes using ps command"""
    try:
        import subprocess
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]
        processes = []
        for line in lines[:20]:  # Limit to 20 processes
            parts = line.split(None, 10)
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "pid": int(parts[1]),
                    "cpu": parts[2],
                    "mem": parts[3],
                    "command": parts[10][:50]  # Truncate command
                })
        return {"total_processes": len(processes), "processes": processes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

