# hash_passwords.py
"""Hash passwords using various algorithms with configurable parameters.

Supported algorithms:
- md5, sha1, sha256 (fast hashes)
- pbkdf2_sha256 (via passlib)
- bcrypt
- scrypt
- argon2 (if available)

The script reads password files from `data/` directory and writes hashed outputs to
`hashed/<algorithm>/<params>/` subfolders.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Callable, Dict

from passlib.hash import pbkdf2_sha256, bcrypt, scrypt, argon2

DATA_DIR = Path(__file__).parent / "data"
HASHED_ROOT = Path(__file__).parent / "hashed"

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def hash_fast(password: str, algo: str) -> str:
    h = getattr(hashlib, algo)()
    h.update(password.encode())
    return h.hexdigest()

def hash_pbkdf2(password: str, iterations: int, salt: bytes) -> str:
    return pbkdf2_sha256.using(rounds=iterations, salt=salt).hash(password)

def hash_bcrypt(password: str, rounds: int) -> str:
    return bcrypt.using(rounds=rounds).hash(password)

def hash_scrypt(password: str, N: int, r: int, p: int, salt: bytes) -> str:
    return scrypt.using(N=N, r=r, p=p, salt=salt).hash(password)

def hash_argon2(password: str, time_cost: int, memory_cost: int, parallelism: int, salt: bytes) -> str:
    return argon2.using(time_cost=time_cost, memory_cost=memory_cost, parallelism=parallelism, salt=salt).hash(password)

HASH_FUNCS: Dict[str, Callable] = {
    "md5": lambda pw, **kw: hash_fast(pw, "md5"),
    "sha1": lambda pw, **kw: hash_fast(pw, "sha1"),
    "sha256": lambda pw, **kw: hash_fast(pw, "sha256"),
    "pbkdf2": hash_pbkdf2,
    "bcrypt": hash_bcrypt,
    "scrypt": hash_scrypt,
    "argon2": hash_argon2,
}

def hash_file(input_path: Path, algo: str, params: dict, output_dir: Path):
    ensure_dir(output_dir)
    with open(input_path, "r", encoding="utf-8") as fin, open(output_dir / f"{input_path.stem}_hashed.txt", "w", encoding="utf-8") as fout:
        for line in fin:
            pwd = line.strip()
            if not pwd:
                continue
            # Prepare common arguments
            salt = params.get("salt", os.urandom(16))
            try:
                hashed = HASH_FUNCS[algo](pwd, **params, salt=salt)
            except Exception as e:
                hashed = f"ERROR:{e}"
            fout.write(hashed + "\n")

def main(config_path: str = "experiment_config.json"):
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    for algo_entry in cfg["hashing_schemes"]:
        algo = algo_entry["algorithm"]
        param_grid = algo_entry.get("params", {})
        # Simple iteration over param combinations (single dict for now)
        params = param_grid
        for pwd_file in DATA_DIR.iterdir():
            if pwd_file.is_file() and pwd_file.suffix == ".txt":
                out_dir = HASHED_ROOT / algo / pwd_file.stem
                hash_file(pwd_file, algo, params, out_dir)
    print("Hashing completed.")

if __name__ == "__main__":
    main()
