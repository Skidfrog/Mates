import streamlit as st
import random

st.set_page_config(page_title="Pràctica de Matemàtiques", page_icon="🧮", layout="centered")

# ---------------------------------------------------------------------------
# Utilitats
# ---------------------------------------------------------------------------

def genera_problema(operacio):
    """Retorna (text_problema, resultat) per a l'operació donada."""
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    if operacio == "Suma":
        resultat = a + b
        signe = "+"
    elif operacio == "Resta":
        if a < b:
            a, b = b, a
        resultat = a - b
        signe = "-"
    elif operacio == "Multiplicació":
        resultat = a * b
        signe = "×"
    elif operacio == "Divisió":
        resultat = random.randint(1, 9)
        b = random.randint(1, 9)
        a = resultat * b
        signe = "÷"
    return f"{a} {signe} {b}", resultat


def anar_a(pantalla):
    st.session_state.screen = pantalla


def tornar_al_menu():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.screen = "menu"


def numpad(entry_key):
    """
    Numpad tàctil + pantalla d'entrada. El valor viu únicament a
    st.session_state[entry_key], gestionat pels botons (mai per un widget
    amb aquesta mateixa key, per evitar el conflicte de Streamlit).
    Retorna True quan es prem "Envia".
    """
    if entry_key not in st.session_state:
        st.session_state[entry_key] = ""

    st.markdown(
        f"""
        <div id="display_{entry_key}" style="
            border: 2px solid #ccc; border-radius: 8px;
            padding: 10px; margin-bottom: 10px;
            font-size: 28px; text-align: center; min-height: 40px;
            font-family: monospace;">
            {st.session_state[entry_key] if st.session_state[entry_key] else '&nbsp;'}
        </div>
        """,
        unsafe_allow_html=True,
    )

    files = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["⌫", "0", "Envia"]]
    enviat = False
    for fila in files:
        cols = st.columns(3)
        for i, val in enumerate(fila):
            label = "✅ Envia" if val == "Envia" else val
            if cols[i].button(label, use_container_width=True, key=f"{entry_key}_{val}"):
                if val == "⌫":
                    st.session_state[entry_key] = st.session_state[entry_key][:-1]
                    st.rerun()
                elif val == "Envia":
                    enviat = True
                else:
                    st.session_state[entry_key] += val
                    st.rerun()

    return enviat


def avanc_automatic(segons=5):
    """
    Passats `segons` segons, fa clic automàticament al botó "Següent ▶️"
    de la pantalla de feedback (si l'usuari no ho ha fet abans manualment).
    El temporitzador viu dins l'iframe del component, així que si l'usuari
    canvia de pantalla abans de temps, aquest iframe desapareix i el
    temporitzador es cancel·la sol (no hi ha avanços fantasma).
    """
    import streamlit.components.v1 as components

    components.html(
        f"""
        <script>
        setTimeout(function() {{
            const botons = window.parent.document.querySelectorAll('button');
            for (const b of botons) {{
                if ((b.innerText || '').includes('Següent')) {{
                    b.click();
                    break;
                }}
            }}
        }}, {int(segons * 1000)});
        </script>
        """,
        height=0,
    )


def activa_dreceres_teclat():
    """
    Injecta un listener global (una sola vegada) que fa que el teclat físic
    funcioni EN QUALSEVOL MOMENT sobre la pàgina, sense haver de clicar cap
    casella abans:
      - Dígits 0-9  -> clic al botó del numpad amb aquell dígit.
      - Retrocés    -> clic al botó "⌫".
      - Intro       -> clic a "Envia" o "Següent" (el que hi hagi visible).
      - Espai       -> clic a "Envia" o "Següent" (el que hi hagi visible).
    Tots els clics es fan sobre els botons reals de Streamlit, així que
    passen per l'únic camí de dades vàlid (el gestor de clic de cada botó).
    """
    import streamlit.components.v1 as components

    components.html(
        """
        <script>
        (function() {
            if (window.parent.__matesKbdBound) { return; }
            window.parent.__matesKbdBound = true;

            function clicaBotoAmbText(match) {
                const botons = window.parent.document.querySelectorAll('button');
                for (const b of botons) {
                    const t = (b.innerText || '').trim();
                    if (match(t)) { b.click(); return true; }
                }
                return false;
            }

            window.parent.document.addEventListener('keydown', function(e) {
                const tag = (e.target && e.target.tagName ? e.target.tagName : '').toLowerCase();
                const enFocusInput = (tag === 'input' || tag === 'textarea');
                if (enFocusInput) { return; }

                if (e.key >= '0' && e.key <= '9') {
                    e.preventDefault();
                    clicaBotoAmbText(t => t === e.key);
                } else if (e.key === 'Backspace') {
                    e.preventDefault();
                    clicaBotoAmbText(t => t === '⌫');
                } else if (e.code === 'Space' || e.key === 'Enter') {
                    e.preventDefault();
                    clicaBotoAmbText(t => t.includes('Envia') || t.includes('Següent'));
                }
            });
        })();
        </script>
        """,
        height=0,
    )


# ---------------------------------------------------------------------------
# Inicialització de l'estat
# ---------------------------------------------------------------------------

if "screen" not in st.session_state:
    st.session_state.screen = "menu"

st.title("🧮 Pràctica de Matemàtiques")
activa_dreceres_teclat()

# ---------------------------------------------------------------------------
# MENU PRINCIPAL
# ---------------------------------------------------------------------------

if st.session_state.screen == "menu":
    st.subheader("Quina operació vols practicar?")
    cols = st.columns(2)
    operacions = ["Suma", "Resta", "Multiplicació", "Divisió"]
    for i, op in enumerate(operacions):
        if cols[i % 2].button(op, use_container_width=True, key=f"menu_{op}"):
            st.session_state.problema, st.session_state.resultat = genera_problema(op)
            st.session_state.operacio = op
            anar_a("problema")
            st.rerun()

    st.write("")
    if st.button("Sèrie de 20", use_container_width=True):
        anar_a("tria_serie")
        st.rerun()

# ---------------------------------------------------------------------------
# PROBLEMA ÚNIC
# ---------------------------------------------------------------------------

elif st.session_state.screen == "problema":
    if "problema_step" not in st.session_state:
        st.session_state.problema_step = "pregunta"

    if st.session_state.problema_step == "pregunta":
        st.subheader(f"Resol: {st.session_state.problema}")

        if numpad("entry_problema"):
            text = st.session_state.entry_problema
            if text != "":
                st.session_state.problema_correcte = int(text) == st.session_state.resultat
            else:
                st.session_state.problema_correcte = None  # resposta no vàlida
            st.session_state.entry_problema = ""
            st.session_state.problema_step = "feedback"
            st.rerun()

        st.write("")
        c1, c2 = st.columns(2)
        if c1.button("Següent ▶️", key="skip_problema"):
            st.session_state.problema, st.session_state.resultat = genera_problema(st.session_state.operacio)
            st.rerun()
        if c2.button("Tornar al menú"):
            tornar_al_menu()
            st.rerun()

    else:  # feedback
        st.subheader(f"Resol: {st.session_state.problema}")
        if st.session_state.problema_correcte is None:
            st.warning("⚠️ Resposta no vàlida")
        elif st.session_state.problema_correcte:
            st.success("✅ Correcte!")
        else:
            st.error(f"❌ Incorrecte. Era {st.session_state.resultat}")

        st.caption("Següent operació en 5 segons... (o prem Espai / Intro / el botó)")
        avanc_automatic(5)

        c1, c2 = st.columns(2)
        if c1.button("Següent ▶️"):
            st.session_state.problema, st.session_state.resultat = genera_problema(st.session_state.operacio)
            st.session_state.problema_step = "pregunta"
            st.rerun()
        if c2.button("Tornar al menú"):
            tornar_al_menu()
            st.rerun()

# ---------------------------------------------------------------------------
# TRIAR OPERACIÓ PER A LA SÈRIE
# ---------------------------------------------------------------------------

elif st.session_state.screen == "tria_serie":
    st.subheader("Quina operació vols per la sèrie de 20?")
    cols = st.columns(2)
    operacions = ["Suma", "Resta", "Multiplicació", "Divisió"]
    for i, op in enumerate(operacions):
        if cols[i % 2].button(op, use_container_width=True, key=f"serie_{op}"):
            st.session_state.serie_operacio = op
            st.session_state.serie_total = 20
            st.session_state.serie_actual = 0
            st.session_state.serie_correctes = 0
            st.session_state.serie_incorrectes = 0
            st.session_state.serie_errors = []
            st.session_state.serie_step = "pregunta"
            anar_a("serie")
            st.rerun()

    st.write("")
    if st.button("Tornar"):
        tornar_al_menu()
        st.rerun()

# ---------------------------------------------------------------------------
# SÈRIE DE 20
# ---------------------------------------------------------------------------

elif st.session_state.screen == "serie":
    if st.session_state.serie_actual >= st.session_state.serie_total and st.session_state.serie_step == "pregunta":
        anar_a("resultat_serie")
        st.rerun()

    if st.session_state.serie_step == "pregunta":
        # Genera problema nou si cal
        if "serie_problema_actual" not in st.session_state:
            st.session_state.serie_actual += 1
            problema, resultat = genera_problema(st.session_state.serie_operacio)
            st.session_state.serie_problema_actual = problema
            st.session_state.serie_resultat_actual = resultat

        st.caption(f"Operació {st.session_state.serie_actual} de {st.session_state.serie_total}")
        st.subheader(f"Resol: {st.session_state.serie_problema_actual}")

        if numpad("entry_serie"):
            text = st.session_state.entry_serie
            resposta_valida = text != ""
            resposta = int(text) if resposta_valida else None
            correcte = resposta_valida and resposta == st.session_state.serie_resultat_actual
            if correcte:
                st.session_state.serie_correctes += 1
            else:
                st.session_state.serie_incorrectes += 1
                mostrat = resposta if resposta_valida else "No vàlida"
                st.session_state.serie_errors.append(
                    (st.session_state.serie_problema_actual, st.session_state.serie_resultat_actual, mostrat)
                )
            st.session_state.serie_ultim_correcte = correcte
            st.session_state.serie_step = "feedback"
            st.session_state.entry_serie = ""
            st.rerun()

        if st.button("Sortir de la sèrie"):
            tornar_al_menu()
            st.rerun()

    elif st.session_state.serie_step == "feedback":
        st.caption(f"Operació {st.session_state.serie_actual} de {st.session_state.serie_total}")
        st.subheader(f"Resol: {st.session_state.serie_problema_actual}")
        if st.session_state.serie_ultim_correcte:
            st.success("✅ Correcte!")
        else:
            st.error(f"❌ Incorrecte. Era {st.session_state.serie_resultat_actual}")

        st.caption("Següent operació en 5 segons... (o prem Espai / Intro / el botó)")
        avanc_automatic(5)

        if st.button("Següent ▶️"):
            del st.session_state.serie_problema_actual
            del st.session_state.serie_resultat_actual
            st.session_state.serie_step = "pregunta"
            st.rerun()

# ---------------------------------------------------------------------------
# RESULTAT DE LA SÈRIE
# ---------------------------------------------------------------------------

elif st.session_state.screen == "resultat_serie":
    st.subheader("Resultat de la sèrie de 20")
    st.write(f"Encerts: {st.session_state.serie_correctes}")
    st.write(f"Errors: {st.session_state.serie_incorrectes}")

    if st.session_state.serie_errors:
        st.write("**Errors:**")
        for prob, sol, user in st.session_state.serie_errors:
            st.write(f"{prob} = {sol} (Tu: {user})")

        if st.button("Repetir només errors"):
            st.session_state.repeat_list = list(st.session_state.serie_errors)
            st.session_state.repeat_index = 0
            st.session_state.repeat_correctes = 0
            st.session_state.repeat_incorrectes = 0
            st.session_state.repeat_errors = []
            st.session_state.repeat_step = "pregunta"
            anar_a("repeticio")
            st.rerun()

    if st.button("Tornar al menú"):
        tornar_al_menu()
        st.rerun()

# ---------------------------------------------------------------------------
# REPETICIÓ D'ERRORS
# ---------------------------------------------------------------------------

elif st.session_state.screen == "repeticio":
    if st.session_state.repeat_index >= len(st.session_state.repeat_list) and st.session_state.repeat_step == "pregunta":
        anar_a("resultat_repeticio")
        st.rerun()

    if st.session_state.repeat_step == "pregunta":
        if "repeat_problema_actual" not in st.session_state:
            prob, sol, _ = st.session_state.repeat_list[st.session_state.repeat_index]
            st.session_state.repeat_index += 1
            st.session_state.repeat_problema_actual = prob
            st.session_state.repeat_resultat_actual = sol

        st.caption(f"Repetició d'errors ({st.session_state.repeat_index} de {len(st.session_state.repeat_list)})")
        st.subheader(f"Resol: {st.session_state.repeat_problema_actual}")

        if numpad("entry_repeat"):
            text = st.session_state.entry_repeat
            resposta_valida = text != ""
            resposta = int(text) if resposta_valida else None
            correcte = resposta_valida and resposta == st.session_state.repeat_resultat_actual
            if correcte:
                st.session_state.repeat_correctes += 1
            else:
                st.session_state.repeat_incorrectes += 1
                mostrat = resposta if resposta_valida else "No vàlida"
                st.session_state.repeat_errors.append(
                    (st.session_state.repeat_problema_actual, st.session_state.repeat_resultat_actual, mostrat)
                )
            st.session_state.repeat_ultim_correcte = correcte
            st.session_state.repeat_step = "feedback"
            st.session_state.entry_repeat = ""
            st.rerun()

        if st.button("Sortir"):
            tornar_al_menu()
            st.rerun()

    elif st.session_state.repeat_step == "feedback":
        st.caption(f"Repetició d'errors ({st.session_state.repeat_index} de {len(st.session_state.repeat_list)})")
        st.subheader(f"Resol: {st.session_state.repeat_problema_actual}")
        if st.session_state.repeat_ultim_correcte:
            st.success("✅ Correcte!")
        else:
            st.error(f"❌ Incorrecte. Era {st.session_state.repeat_resultat_actual}")

        st.caption("Següent operació en 5 segons... (o prem Espai / Intro / el botó)")
        avanc_automatic(5)

        if st.button("Següent ▶️"):
            del st.session_state.repeat_problema_actual
            del st.session_state.repeat_resultat_actual
            st.session_state.repeat_step = "pregunta"
            st.rerun()

# ---------------------------------------------------------------------------
# RESULTAT DE LA REPETICIÓ
# ---------------------------------------------------------------------------

elif st.session_state.screen == "resultat_repeticio":
    st.subheader("Resultat de la repetició")
    st.write(f"Encerts: {st.session_state.repeat_correctes}")
    st.write(f"Errors: {st.session_state.repeat_incorrectes}")

    if st.session_state.repeat_errors:
        st.write("**Errors:**")
        for prob, sol, user in st.session_state.repeat_errors:
            st.write(f"{prob} = {sol} (Tu: {user})")

    if st.button("Tornar al menú"):
        tornar_al_menu()
        st.rerun()
