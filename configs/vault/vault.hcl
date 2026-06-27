# =====================================================
# Versio Local Persistent Vault Configuration
# =====================================================

ui = true

disable_mlock = true

storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = true
}

api_addr = "http://0.0.0.0:8200"
