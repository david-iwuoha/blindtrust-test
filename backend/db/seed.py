# backend/db/seed.py
from .crud_users import create_user, get_user_by_username
from .crud_beneficiaries import add_beneficiary
from .connection import get_db_conn, init_db_from_schema

def seed_demo():
    init_db_from_schema()

    # create demo user
    demo_username = "demo_user"
    demo = get_user_by_username(demo_username)
    if not demo:
        demo = create_user(username=demo_username, phone="08000000000", gender="unknown", language="en-NG")

    # create recipient users
    for uname in ["demo-acc-john", "demo-acc-mary"]:
        if not get_user_by_username(uname):
            create_user(username=uname)

    # add beneficiaries to demo_user
    add_beneficiary(demo["id"], "john", alias="John Doe", account_ref="demo-acc-john")
    add_beneficiary(demo["id"], "mary", alias="Mary Jane", account_ref="demo-acc-mary")

    return demo
