#!/bin/bash
# MCP Server Wrapper - 自动刷新 Token 并启动服务器
# 此脚本会自动从 Azure CLI 获取最新的 Fabric Token

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 获取最新的 Fabric Token
export FABRIC_TOKEN=$(az account get-access-token --resource "https://api.fabric.microsoft.com" --query accessToken -o tsv 2>/dev/null)

if [ -z "$FABRIC_TOKEN" ]; then
    echo "警告: 无法获取 Fabric Token，请确保已运行 'az login'" >&2
    export FABRIC_AUTH_METHOD="simulation"
else
    export FABRIC_AUTH_METHOD="bearer_token"
fi

# 启动 MCP 服务器
exec node "$PROJECT_DIR/build/index.js"
