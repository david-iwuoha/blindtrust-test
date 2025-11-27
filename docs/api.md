# BlindTrust API Specification

## AUTH
- /auth/google-login

## USER
- /user/me
- /user/update-language

## ACCOUNTS
- /accounts/balance
- /accounts/transfer
- /accounts/undo

## BENEFICIARIES
- /beneficiaries/add
- /beneficiaries/list
- /beneficiaries/remove

## AI
- /ai/process

uvicorn backend.main:app --reload --port 8001
