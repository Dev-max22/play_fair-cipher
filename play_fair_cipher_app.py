import streamlit as st

# ─────────────────────────────────────────────
# PLAYFAIR CIPHER LOGIC
# ─────────────────────────────────────────────

def build_grid(keyword):
    keyword = keyword.upper().replace("J", "I")
    seen = []
    for ch in keyword:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in seen:
            seen.append(ch)
    return [seen[i*5:(i+1)*5] for i in range(5)]


def find_position(grid, letter):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == letter:
                return r, c
    return None


def prepare_plaintext(text):
    text = text.upper().replace("J", "I")
    text = "".join(ch for ch in text if ch.isalpha())
    digraphs = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 == len(text):
            digraphs.append((a, "X"))
            i += 1
        elif text[i] == text[i + 1]:
            digraphs.append((a, "X"))
            i += 1
        else:
            digraphs.append((a, text[i + 1]))
            i += 2
    return digraphs


def prepare_ciphertext(text):
    text = text.upper().replace("J", "I")
    text = "".join(ch for ch in text if ch.isalpha())
    if len(text) % 2 != 0:
        text += "X"
    return [(text[i], text[i+1]) for i in range(0, len(text), 2)]


def encrypt_pair(grid, a, b):
    r1, c1 = find_position(grid, a)
    r2, c2 = find_position(grid, b)
    if r1 == r2:
        rule = "Same Row - Shift Right"
        enc_a = grid[r1][(c1 + 1) % 5]
        enc_b = grid[r2][(c2 + 1) % 5]
    elif c1 == c2:
        rule = "Same Column - Shift Down"
        enc_a = grid[(r1 + 1) % 5][c1]
        enc_b = grid[(r2 + 1) % 5][c2]
    else:
        rule = "Rectangle - Swap Corners"
        enc_a = grid[r1][c2]
        enc_b = grid[r2][c1]
    return enc_a, enc_b, rule


def decrypt_pair(grid, a, b):
    r1, c1 = find_position(grid, a)
    r2, c2 = find_position(grid, b)
    if r1 == r2:
        rule = "Same Row - Shift Left"
        dec_a = grid[r1][(c1 - 1) % 5]
        dec_b = grid[r2][(c2 - 1) % 5]
    elif c1 == c2:
        rule = "Same Column - Shift Up"
        dec_a = grid[(r1 - 1) % 5][c1]
        dec_b = grid[(r2 - 1) % 5][c2]
    else:
        rule = "Rectangle - Swap Corners"
        dec_a = grid[r1][c2]
        dec_b = grid[r2][c1]
    return dec_a, dec_b, rule


def encrypt(keyword, plaintext):
    grid = build_grid(keyword)
    digraphs = prepare_plaintext(plaintext)
    steps = []
    cipher = []
    for a, b in digraphs:
        enc_a, enc_b, rule = encrypt_pair(grid, a, b)
        steps.append({"pair": f"{a}{b}", "rule": rule, "result": f"{enc_a}{enc_b}"})
        cipher.append(enc_a + enc_b)
    return grid, digraphs, steps, " ".join(cipher)


def decrypt(keyword, ciphertext):
    grid = build_grid(keyword)
    digraphs = prepare_ciphertext(ciphertext)
    steps = []
    plain = []
    for a, b in digraphs:
        dec_a, dec_b, rule = decrypt_pair(grid, a, b)
        steps.append({"pair": f"{a}{b}", "rule": rule, "result": f"{dec_a}{dec_b}"})
        plain.append(dec_a + dec_b)
    return grid, digraphs, steps, " ".join(plain)


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Playfair Cipher",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("📖 Instructions")
    st.markdown("Welcome to the **Playfair Cipher Encryptor!**")
    st.divider()

    with st.expander("🤔 What is Playfair Cipher?"):
        st.markdown(
            "The Playfair Cipher is a **classical encryption technique** that encrypts "
            "**two letters at a time** (called digraphs) using a 5x5 key grid.\n\n"
            "It was invented by **Charles Wheatstone in 1854** but became popular "
            "through **Lord Playfair**, which is why it carries his name.\n\n"
            "It was even used by the **British military in World War I.**"
        )

    with st.expander("🚀 How to Use This App"):
        st.markdown(
            "1. Enter a **Keyword** — any word you like, this builds your secret 5x5 grid\n\n"
            "2. Enter your **message** (plaintext to encrypt, or ciphertext to decrypt)\n\n"
            "3. Choose **Encrypt** or **Decrypt**\n\n"
            "4. The app will show you the **grid**, **digraphs**, **step by step** breakdown and the final **result**"
        )

    with st.expander("📏 The 3 Encryption Rules"):
        st.markdown("**Rule 1 — Same Row: Shift Right (Encrypt) / Left (Decrypt)**")
        st.markdown(
            "If both letters are in the **same row**, shift each letter "
            "**one step to the right** to encrypt (left to decrypt). Wraps around."
        )
        st.code("Encrypt: ON → NA\nDecrypt: NA → ON")

        st.markdown("---")

        st.markdown("**Rule 2 — Same Column: Shift Down (Encrypt) / Up (Decrypt)**")
        st.markdown(
            "If both letters are in the **same column**, shift each letter "
            "**one step downward** to encrypt (upward to decrypt). Wraps around."
        )
        st.code("Encrypt: OF → HP\nDecrypt: HP → OF")

        st.markdown("---")

        st.markdown("**Rule 3 — Rectangle: Swap Corners (same for both)**")
        st.markdown(
            "If the two letters form a rectangle, each letter **stays on its own row** "
            "but **jumps to the column of the other letter**. Same for encrypt and decrypt."
        )
        st.code("Example: MH → OC")

    with st.expander("💡 Tips"):
        st.markdown(
            "- **J** is always replaced with **I** before encrypting\n\n"
            "- If a pair has **two identical letters** (e.g. LL), insert **X** between them → LX\n\n"
            "- If the message ends with a **single unpaired letter**, add **X** to complete the pair\n\n"
            "- Both sender and receiver must share the **same keyword** to decrypt\n\n"
            "- The keyword should be kept **secret** — it is your encryption key"
        )

    with st.expander("📝 Example"):
        st.markdown("**Keyword:** SUPERMAN")
        st.markdown("**Plaintext:** HELLO")
        st.markdown("**After preparing digraphs:** HE | LX | OX")
        st.markdown("---")
        st.markdown("**HE** → Same Column → **BQ**")
        st.markdown("**LX** → Rectangle → **OW**")
        st.markdown("**OX** → Same Column → **XP**")
        st.markdown("---")
        st.markdown("**Final Ciphertext: BQ OW XP**")

    st.divider()
    st.caption("Built with love using Streamlit")

# ─────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────

st.title("🔐 Playfair Cipher")
st.markdown("Enter a **keyword** and a **message** to encrypt or decrypt using the Playfair Cipher.")

st.divider()

col1, col2 = st.columns(2)
with col1:
    keyword = st.text_input("🗝️ Keyword", placeholder="e.g. SUPERMAN")
with col2:
    message = st.text_input("📝 Message", placeholder="e.g. HELLO")

col_enc, col_dec = st.columns(2)
with col_enc:
    encrypt_btn = st.button("🔒 Encrypt", use_container_width=True, type="primary")
with col_dec:
    decrypt_btn = st.button("🔓 Decrypt", use_container_width=True, type="secondary")

# ─────────────────────────────────────────────
# ENCRYPT
# ─────────────────────────────────────────────
if encrypt_btn:
    if not keyword.strip():
        st.error("Please enter a keyword!")
    elif not message.strip():
        st.error("Please enter a message!")
    else:
        grid, digraphs, steps, cipher_spaced = encrypt(keyword.strip(), message.strip())

        st.divider()

        st.subheader("📊 5x5 Key Grid")
        st.markdown(f"Built from keyword: **{keyword.upper()}**")

        style = (
            "<style>"
            ".grid-table { border-collapse: collapse; margin: 10px auto; }"
            ".grid-table td {"
            "  width: 48px; height: 48px;"
            "  text-align: center; vertical-align: middle;"
            "  font-size: 20px; font-weight: bold;"
            "  border: 2px solid #4a4a8a;"
            "  background: #1e1e3f;"
            "  color: #e0e0ff;"
            "  border-radius: 6px;"
            "}"
            ".grid-header {"
            "  background: #3a3a6a !important;"
            "  color: #aaaaff !important;"
            "  font-size: 13px !important;"
            "  font-weight: normal !important;"
            "}"
            "</style>"
        )

        grid_html = style + "<table class='grid-table'>"
        grid_html += "<tr><td class='grid-header'></td>"
        for c in range(1, 6):
            grid_html += f"<td class='grid-header'>C{c}</td>"
        grid_html += "</tr>"
        for i, row in enumerate(grid):
            grid_html += f"<tr><td class='grid-header'>R{i+1}</td>"
            for ch in row:
                grid_html += f"<td>{ch}</td>"
            grid_html += "</tr>"
        grid_html += "</table>"

        st.markdown(grid_html, unsafe_allow_html=True)

        st.divider()

        st.subheader("✂️ Prepared Digraphs")
        pairs_display = "  |  ".join([f"**{a}{b}**" for a, b in digraphs])
        st.markdown(pairs_display)

        st.divider()

        st.subheader("🔄 Encryption Steps")
        for i, step in enumerate(steps):
            with st.expander(f"Pair {i+1}: {step['pair']} → {step['result']}", expanded=True):
                st.markdown(f"- **Rule Applied:** {step['rule']}")
                st.markdown(f"- **Input Pair:** `{step['pair']}`")
                st.markdown(f"- **Encrypted Pair:** `{step['result']}`")

        st.divider()

        st.subheader("🔐 Ciphertext")
        st.metric("Encrypted Text", cipher_spaced)
        st.success(f"'{message.upper()}' encrypted successfully using key '{keyword.upper()}'!")

# ─────────────────────────────────────────────
# DECRYPT
# ─────────────────────────────────────────────
if decrypt_btn:
    if not keyword.strip():
        st.error("Please enter a keyword!")
    elif not message.strip():
        st.error("Please enter a ciphertext message!")
    else:
        grid, digraphs, steps, plain_spaced = decrypt(keyword.strip(), message.strip())

        st.divider()

        st.subheader("📊 5x5 Key Grid")
        st.markdown(f"Built from keyword: **{keyword.upper()}**")

        style = (
            "<style>"
            ".grid-table { border-collapse: collapse; margin: 10px auto; }"
            ".grid-table td {"
            "  width: 48px; height: 48px;"
            "  text-align: center; vertical-align: middle;"
            "  font-size: 20px; font-weight: bold;"
            "  border: 2px solid #4a4a8a;"
            "  background: #1e1e3f;"
            "  color: #e0e0ff;"
            "  border-radius: 6px;"
            "}"
            ".grid-header {"
            "  background: #3a3a6a !important;"
            "  color: #aaaaff !important;"
            "  font-size: 13px !important;"
            "  font-weight: normal !important;"
            "}"
            "</style>"
        )

        grid_html = style + "<table class='grid-table'>"
        grid_html += "<tr><td class='grid-header'></td>"
        for c in range(1, 6):
            grid_html += f"<td class='grid-header'>C{c}</td>"
        grid_html += "</tr>"
        for i, row in enumerate(grid):
            grid_html += f"<tr><td class='grid-header'>R{i+1}</td>"
            for ch in row:
                grid_html += f"<td>{ch}</td>"
            grid_html += "</tr>"
        grid_html += "</table>"

        st.markdown(grid_html, unsafe_allow_html=True)

        st.divider()

        st.subheader("✂️ Ciphertext Digraphs")
        pairs_display = "  |  ".join([f"**{a}{b}**" for a, b in digraphs])
        st.markdown(pairs_display)

        st.divider()

        st.subheader("🔄 Decryption Steps")
        for i, step in enumerate(steps):
            with st.expander(f"Pair {i+1}: {step['pair']} → {step['result']}", expanded=True):
                st.markdown(f"- **Rule Applied:** {step['rule']}")
                st.markdown(f"- **Input Pair:** `{step['pair']}`")
                st.markdown(f"- **Decrypted Pair:** `{step['result']}`")

        st.divider()

        st.subheader("🔓 Plaintext")
        st.metric("Decrypted Text", plain_spaced)
        st.success(f"'{message.upper()}' decrypted successfully using key '{keyword.upper()}'!")
