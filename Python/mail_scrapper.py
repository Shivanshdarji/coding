import imaplib
import email
import getpass
from email.header import decode_header

IMAP_SERVER = "imap.gmail.com"
EMAIL_ACCOUNT = "23ce84@svitvasad.ac.in"
#phonon.io=bfrp adxv zvge zdur
print("=" * 60)
print("Gmail IMAP Login - Email CC Scraper")
print("=" * 60)
print(f"Account: {EMAIL_ACCOUNT}")
print()
print("  You need an App Password (NOT your regular password).")
print(f"   1. Go to: https://myaccount.google.com/apppasswords")
print(f"   2. Make sure you're logged in as {EMAIL_ACCOUNT}")
print(f"   3. Generate an App Password for 'Mail'")
print(f"   4. Use that 16-character password below")
print("=" * 60)

# getpass fails in VS Code terminal — fall back to plain input
try:
    APP_PASSWORD = getpass.getpass("Enter App Password (hidden): ")
except (KeyboardInterrupt, Exception):
    print()
    APP_PASSWORD = input("Enter App Password (visible fallback): ")

# ── Connect ──────────────────────────────────────────────────
print("\n[LOG] Connecting to IMAP server...")
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
print("[LOG] Connected. Logging in...")
mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
print("[LOG] Login successful.\n")

# ── Discover all folders ──────────────────────────────────────
print("[LOG] Fetching folder list...")
_, folder_list = mail.list()
folders = []
for f in folder_list:
    parts = f.decode().split('"/"')
    folder_name = parts[-1].strip().strip('"')
    folders.append(folder_name)
print(f"[LOG] Found {len(folders)} folders: {', '.join(folders)}\n")

# ── Scan every folder ─────────────────────────────────────────
cc_emails_found = 0
seen_message_ids = set()

for folder_idx, folder in enumerate(folders, 1):
    print(f"[LOG] [{folder_idx}/{len(folders)}] Opening folder: {folder}")
    try:
        status, _ = mail.select(f'"{folder}"', readonly=True)
        if status != "OK":
            print(f"[LOG]   ↳ Skipped (could not select).")
            continue

        status, messages = mail.search(None, f'HEADER Cc "{EMAIL_ACCOUNT}"')
        if status != "OK":
            print(f"[LOG]   ↳ Skipped (search failed).")
            continue

        email_ids = messages[0].split()
        total_in_folder = len(email_ids)
        print(f"[LOG]   ↳ {total_in_folder} emails to scan...")

        for i, e_id in enumerate(email_ids, 1):
            # Progress every 50 emails
            if i % 50 == 0 or i == total_in_folder:
                print(f"[LOG]   ↳ Progress: {i}/{total_in_folder} emails checked, {cc_emails_found} CC matches so far")

            res, msg_data = mail.fetch(e_id, "(RFC822)")
            if res != "OK":
                continue

            for response_part in msg_data:
                if not isinstance(response_part, tuple):
                    continue

                msg = email.message_from_bytes(response_part[1])

                # Deduplicate
                message_id = msg.get("Message-ID", "")
                if message_id and message_id in seen_message_ids:
                    continue

                # Case-insensitive CC check
                cc_header = msg.get("Cc", "") or ""
                if EMAIL_ACCOUNT.lower() not in cc_header.lower():
                    continue

                if message_id:
                    seen_message_ids.add(message_id)

                cc_emails_found += 1

                # Decode Subject
                raw_subject = msg.get("Subject", "(No Subject)")
                subject_parts = decode_header(raw_subject)
                subject_decoded, enc = subject_parts[0]
                if isinstance(subject_decoded, bytes):
                    subject_decoded = subject_decoded.decode(enc or "utf-8", errors="replace")

                print(f"\n  ✅ Email #{cc_emails_found} (CC match found!)")
                print(f"     Folder : {folder}")
                print(f"     Subject: {subject_decoded}")
                print(f"     From   : {msg['From']}")
                print(f"     To     : {msg['To']}")
                print(f"     CC     : {cc_header}")
                print(f"     Date   : {msg['Date']}")

                # Extract body
                body_text = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                body_text = part.get_payload(decode=True).decode(errors="replace")
                            except Exception:
                                pass
                            break
                else:
                    try:
                        body_text = msg.get_payload(decode=True).decode(errors="replace")
                    except Exception:
                        pass

                print(f"     Body   : {body_text[:300]}{'...' if len(body_text) > 300 else ''}\n")

    except Exception as e:
        print(f"[LOG]   ↳ Error in folder '{folder}': {e}")
        continue

# ── Summary ───────────────────────────────────────────────────
print("\n" + "=" * 60)
if cc_emails_found == 0:
    print("No emails found where you are in CC.")
else:
    print(f"✅ Total unique emails where you are in CC: {cc_emails_found}")
print("=" * 60)

mail.close()
mail.logout()
print("[LOG] Done. Connection closed.")

