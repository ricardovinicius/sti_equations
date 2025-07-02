import streamlit as st

import solver

from pages.problems import set_random_problem
from streamlit_app import get_data, save_data

def parse_user_input(input_str):
    try:
        return float(input_str)
    except ValueError:
        if '/' in input_str:
            try:
                numerator, denominator = map(float, input_str.split('/'))
                if denominator == 0:
                    return None  # Division by zero
                return numerator / denominator
            except ValueError:
                return None  # Not a valid fraction format
        return None  # Not a valid number or fraction

change_type_tips = {
    # Transformações diretamente usadas para isolar x
    "ADD_TO_BOTH_SIDES": "Adicione o mesmo valor aos dois lados da equação.",
    "SUBTRACT_FROM_BOTH_SIDES": "Subtraia o mesmo valor dos dois lados da equação.",
    "MULTIPLY_TO_BOTH_SIDES": "Multiplique os dois lados da equação pelo mesmo valor.",
    "DIVIDE_FROM_BOTH_SIDES": "Divida os dois lados da equação pelo mesmo valor.",
    "MULTIPLY_BOTH_SIDES_BY_INVERSE_FRACTION": "Multiplique ambos os lados pelo inverso da fração.",
    "MULTIPLY_BOTH_SIDES_BY_NEGATIVE_ONE": "Multiplique os dois lados por -1 para trocar o sinal.",
    "SWAP_SIDES": "Troque os lados da equação para facilitar a leitura.",

    # Simplificações algébricas comuns
    "SIMPLIFY_ARITHMETIC": "Resolva contas simples (como somas ou multiplicações).",
    "SIMPLIFY_LEFT_SIDE": "Simplifique a expressão do lado esquerdo.",
    "SIMPLIFY_RIGHT_SIDE": "Simplifique a expressão do lado direito.",
    "COLLECT_AND_COMBINE_LIKE_TERMS": "Agrupe e some os termos semelhantes.",
    "COLLECT_LIKE_TERMS": "Agrupe os termos semelhantes.",
    "REARRANGE_COEFF": "Reorganize os coeficientes para facilitar a leitura.",
    "ADD_POLYNOMIAL_TERMS": "Some os termos do polinômio que são semelhantes.",
    "ADD_COEFFICIENT_OF_ONE": "Adicione o coeficiente 1 onde ele está implícito.",
    "UNARY_MINUS_TO_NEGATIVE_ONE": "Converta o sinal de menos para -1 vezes o termo.",
    "REMOVE_ADDING_ZERO": "Remova a adição de zero, pois não altera o valor.",
    "REMOVE_MULTIPLYING_BY_ONE": "Remova a multiplicação por 1, pois não altera o valor.",
    "REMOVE_MULTIPLYING_BY_NEGATIVE_ONE": "Remova a multiplicação por -1 ao simplificar o sinal.",
    "RESOLVE_DOUBLE_MINUS": "Dois sinais de menos se anulam: transforme em mais.",

    # Simplificações envolvendo frações
    "SIMPLIFY_FRACTION": "Simplifique a fração dividindo numerador e denominador por um fator comum.",
    "SIMPLIFY_SIGNS": "Ajuste os sinais da fração (ex: -a/-b = a/b).",
    "CANCEL_TERMS": "Cancele termos iguais no numerador e denominador.",
    "CANCEL_MINUSES": "Elimine sinais de menos duplicados.",
    "MULTIPLY_BY_INVERSE": "Multiplique por uma fração invertida para facilitar a resolução.",

    # Verificação de conclusão
    "STATEMENT_IS_TRUE": "A equação foi resolvida corretamente (verdadeiro).",
    "STATEMENT_IS_FALSE": "A equação não tem solução (falsa)."
}

# Main page content
st.markdown("# Math Tutor: First-Degree Equations")
st.sidebar.markdown("# Main page 🎈")

# Inicializa estados
if "current_problem" not in st.session_state:
    st.session_state.current_problem = ""
if "solve_for" not in st.session_state:
    st.session_state.solve_for = ""
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""
if "hint_pos" not in st.session_state:
    st.session_state.hint_pos = 0
if "solution_steps" not in st.session_state:
    st.session_state.solution_steps = solver.get_equation_solve_steps(st.session_state.current_problem)
if "problem_difficulty" not in st.session_state:
    st.session_state.problem_difficulty = 1

if st.session_state.current_problem == "":
    set_random_problem()

# Função para exibir uma dica (simulação)
def mostrar_dica():
    # Reset hint_pos to 0 if it's at or beyond the last hint
    if st.session_state.hint_pos >= len(st.session_state.solution_steps):
        st.session_state.hint_pos = 0

    # Display the current hint
    st.info(change_type_tips[st.session_state.solution_steps[st.session_state.hint_pos]["changeType"]])

    # Increment hint_pos for the next hint
    st.session_state.hint_pos += 1

@st.dialog("Solução")
def display_result(result):
    if result:
        map_difficult = {
            1: "Fácil",
            2: "Intermediário",
            3: "Difícil"
        }

        st.balloons()
        user_data = get_data()
        pontos = 5 * st.session_state.problem_difficulty - (st.session_state.hint_pos + 1)
        user_data["pontos"] += pontos
        user_data["resolvidos"] += 1
        user_data["por_dificuldade"][map_difficult[st.session_state.problem_difficulty]] += 1
        save_data(user_data)
        st.success("Parabéns. Solução correta. Tente um novo problema.")
        st.info(f"Pontos ganhos: {pontos}")

        # Limpa a resposta e define um novo problema
        st.session_state.user_answer = ""
        set_random_problem()

    else:
        st.error("Solução incorreta. Tente novamente, ou utilize dicas.")


with st.container(border=True):
    # Título com emoji
    st.markdown("### 🧠 Problema Atual")

    # Exibição do problema
    st.markdown(f"**Equação:**")
    st.markdown(f"#### {st.session_state.current_problem}")
    st.caption(f"**Resolva para:** `{st.session_state.solve_for}`")

    with st.form('problem'):
        st.session_state.user_answer = st.text_input("Sua resposta:", key=f"answer_input_{st.session_state.current_problem}")
        submit = st.form_submit_button('Enviar solução')

    if submit:
        parsed_answer = parse_user_input(st.session_state.user_answer)
        if parsed_answer is None:
            st.error("Por favor, insira um número válido ou uma fração (ex: 1/2).")
        else:
            is_correct = abs(
                solver.get_equation_solution(st.session_state.current_problem, st.session_state.solve_for) - parsed_answer
            ) <= 0.0001
            
            display_result(is_correct)
            
            if is_correct:
                st.rerun()

    # Botões adicionais
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💡 Obter uma dica"):
            mostrar_dica()

    with col2:
        if st.button("🔄 Novo problema"):
            set_random_problem()

