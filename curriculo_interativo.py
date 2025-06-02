import streamlit as st
from urllib.parse import parse_qs

# Base simplificada da grade com exemplos reais de Engenharia Elétrica no Brasil
disciplinas = {
    # 1º Semestre
    "EEL7011": {"nome": "Laboratório de Eletricidade Básica", "semestre": 1, "pre": [], "carga": 36},
    "EEL7014": {"nome": "Introdução às Engenharias Elétrica e Eletrônica", "semestre": 1, "pre": [], "carga": 36},
    "FSC5101": {"nome": "Física 1", "semestre": 1, "pre": [], "carga": 72},
    "LLV7801": {"nome": "Produção Textual Acadêmica", "semestre": 1, "pre": [], "carga": 72},
    "MTM3100": {"nome": "Pré-Cálculo", "semestre": 1, "pre": [], "carga": 72},
    "MTM3101": {"nome": "Cálculo 1", "semestre": 1, "pre": [], "carga": 72},
    "MTM3111": {"nome": "Geometria Analítica", "semestre": 1, "pre": [], "carga": 72},
    "QMC5125": {"nome": "Química Geral Experimental A ", "semestre": 1, "pre": [], "carga": 36},
    "QMC5138": {"nome": "Química Geral", "semestre": 1, "pre": [], "carga": 36},

    # 2º Semestre
    "EGR5619": {"nome": "Desenho Técnico para Engenharia Elétrica", "semestre": 2, "pre": [], "carga": 72},
    "FSC5002": {"nome": "Física II", "semestre": 2, "pre": ["FSC5101","MTM3101"], "carga": 72},
    "FSC5122": {"nome": "Física Experimental 1", "semestre": 2, "pre": ["FSC5101"], "carga": 54},
    "INE5201": {"nome": "Introdução à Ciência da Computação", "semestre": 2, "pre": [], "carga": 54},
    "MTM3102": {"nome": "Cálculo 2", "semestre": 2, "pre": ["MTM3101"], "carga": 72},
    "MTM3112": {"nome": "Álgebra Linear", "semestre": 2, "pre": ["MTM3111"], "carga": 72},

    # 3º Semestre
    "ELE3001": {"nome": "Conservação de Recursos Naturais", "semestre": 3, "pre": [], "carga": 36},
    "EEL5105": {"nome": "Circuitos e Técnicas Digitais", "semestre": 3, "pre": ["EEL7011"], "carga": 90},
    "EEL7013": {"nome": "Laboratório de Transdutores", "semestre": 3, "pre": ["EEL7011"], "carga": 36},
    "FSC5113": {"nome": "Física III", "semestre": 3, "pre": ["FSC5002"], "carga": 72},
    "INE5118": {"nome": "Probabilidade Estatística e Processos Estocásticos", "semestre": 3, "pre": ["MTM3102"], "carga": 72},
    "INE5202": {"nome": "Cálculo Numérico em Computadores", "semestre": 3, "pre": ["INE5201","MTM3102","MTM3112"], "carga": 72},
    "MTM3103": {"nome": "Cálculo 3", "semestre": 3, "pre": ["MTM3102","MTM3111"], "carga": 72},

    # 4º Semestre
    "EEL7030": {"nome": "Microprocessadores", "semestre": 4, "pre": ["EEL5105"], "carga": 72},
    "EEL7041": {"nome": "Eletromagnetismo", "semestre": 4, "pre": ["FSC5113","MTM3103"], "carga": 72},
    "EEL7045": {"nome": "Circuitos Elétricos A", "semestre": 4, "pre": ["EEL7013","FSC5113","MTM3102"], "carga": 108},
    "EPS7019": {"nome": "Engenharia Econômica", "semestre": 4, "pre": ["900 hs"], "carga": 54},
    "FSC5114": {"nome": "Física IV", "semestre": 4, "pre": ["FSC5113"], "carga": 72},
    "MTM3104": {"nome": "Cálculo 4", "semestre": 4, "pre": ["MTM3102"], "carga": 72},

    # 5º Semestre
    "EEL7051": {"nome": "Materiais Elétricos", "semestre": 5, "pre": ["FSC5114","QMC5125","QMC5138"], "carga": 72},
    "EEL7052": {"nome": "Sistemas Lineares", "semestre": 5, "pre": ["EEL7045","MTM3104","MTM3112"], "carga": 90},
    "EEL7053": {"nome": "Ondas Eletromagnéticas", "semestre": 5, "pre": ["EEL7041","EEL7045"], "carga": 72},
    "EEL7055": {"nome": "Circuitos Elétricos B", "semestre": 5, "pre": ["EEL7045"], "carga": 108},
    "EEL7061": {"nome": "Eletrônica I", "semestre": 5, "pre": ["EEL7045","FSC5114"], "carga": 108},

    # 6º Semestre
    "DIR5998": {"nome": "Legislação e Ética em Engenharia Elétrica", "semestre": 6, "pre": ["1200 hs"], "carga": 36},
    "EEL7062": {"nome": "Princípios de Sistemas de Comunicação", "semestre": 6, "pre": ["EEL7052","INE5118"], "carga": 90},
    "EEL7063": {"nome": "Sistemas de Controle", "semestre": 6, "pre": ["EEL7052"], "carga": 108},
    "EEL7064": {"nome": "Conversão Eletromecânica de Energia A ", "semestre": 6, "pre": ["EEL7041","EEL7051","EEL7055"], "carga": 72},
    "EEL7072": {"nome": "Projeto de Instalações Elétricas", "semestre": 6, "pre": ["EEL7051","EEL7055"], "carga": 72},
    "EEL7522": {"nome": "Processamento Digital de Sinais", "semestre": 6, "pre": ["EEL7052"], "carga": 72},

    # 7º Semestre
    "EEL7071": {"nome": "Introdução a Sistemas de Energia Elétrica", "semestre": 7, "pre": ["EEL7053","EEL7064","INE5202"], "carga": 72},
    "EEL7073": {"nome": "Conversão Eletromecânica de Energia B", "semestre": 7, "pre": ["EEL7064"], "carga": 72},
    "EEL7074": {"nome": "Eletrônica de Potencia I", "semestre": 7, "pre": ["EEL7061"], "carga": 90},
    "EEL7300": {"nome": "Instrumentação Eletrônica", "semestre": 7, "pre": ["EEL5105","EEL7061"], "carga": 90},
    "EMC5425": {"nome": "Fenômenos de Transportes", "semestre": 7, "pre": ["FSC5113","FSC5122","MTM3103"], "carga": 72},
    "INE5407": {"nome": "Ciência, Tecnologia e Sociedade", "semestre": 7, "pre": ["1200 hs"], "carga": 54},

    # 8º Semestre
    "EEL7080": {"nome": "Seminários de Engenharia Elétrica", "semestre": 8, "pre": ["EEL7055","LLV7801","72 hs Ob"], "carga": 36},
    "EEL7081": {"nome": "Aspectos de Segurança em Engenharia Elétrica", "semestre": 8, "pre": ["EEL7072"], "carga": 36},
    "--": {"nome": "Optativa", "semestre": 8, "pre": [], "carga": 360},

    # 9º Semestre
    "EEL7830": {"nome": "Estágio Curricular Curto I", "semestre": 9, "pre": ["2000 hs"], "carga": 180},
    "EEL7871": {"nome": "Estágio Curricular Curto II", "semestre": 9, "pre": ["EEL7830","144 hs"], "carga": 180},
    "EEL7872": {"nome": "Estágio Curricular Longo", "semestre": 9, "pre": ["2000 hs"], "carga": 360},
    "EEL7889": {"nome": "Planejamento do Trabalho de conclusão de Curso", "semestre": 9, "pre": ["144 hs"], "carga": 36},
    "-": {"nome": "Optativa", "semestre": 9, "pre": ["2000 hs"], "carga": 72},
    
    # 10º Semestre
    "EEL7890": {"nome": "Trabalho de Conclusão de Curso (TCC)", "semestre": 10, "pre": ["EEL7889","216 hs"], "carga": 324}
}

st.set_page_config(layout="wide",
                   page_title="UFSC - Engenharia Elétrica",
                   page_icon=":zap:", 
                   initial_sidebar_state="collapsed",
                   )

# Adicionar CSS para centralizar o título E reduzir o espaço acima
st.markdown("""
<style>
    /* Centralizar título */
    h1 {
        text-align: center;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Reduzir espaço acima do conteúdo principal */
    .main .block-container {
        padding-top: 1rem !important;
    }
    
    /* Remover espaços extras do cabeçalho Streamlit */
    header.css-18ni7ap.e8zbici2 {
        visibility: hidden;
        height: 0;
        padding: 0;
        margin: 0;
    }
    
    /* Ajustar margens globais */
    .stApp {
        margin-top: -4rem;
    }
</style>
""", unsafe_allow_html=True)

# Adicionar CSS para centralizar o título
st.markdown("""
<style>
    h1 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Usar o st.title normalmente - agora será centralizado
st.title("Grade Curricular Interativa - :blue[Engenharia Elétrica]")

# Criar duas colunas para colocar "Como usar" e a legenda lado a lado
col_info, col_legenda = st.columns([1, 3])

# Na primeira coluna, colocar o "Como usar" centralizado e sem quebra de linha
with col_info:
    st.markdown("""
    <div style="
                border-radius:4px; 
                padding:0.3rem 0.5rem; 
                margin-bottom:0.1rem; 
                font-size:0.85em; 
                display:flex; 
                align-items:center;
                justify-content: center;
                height: 100%;">
        <span style="color:#1565c0; margin-right:6px;">ℹ️</span>
        <span style="white-space:nowrap;"><b>Como usar:</b> Clique em uma disciplina para visualizar suas relações.</span>
    </div>
    """, unsafe_allow_html=True)

# Na segunda coluna, colocar a legenda centralizada
with col_legenda:
    # Versão horizontal da legenda com centralização
    legenda_compacta = """
    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; justify-content:center; height: 100%;">
      <span style="font-weight:bold; font-size:0.85em; white-space:nowrap;">Legenda:</span>
      <div style="display:inline-flex; align-items:center; margin:0 2px;">
        <span style="color:#006400; font-weight:bold; margin-right:3px;">■</span>
        <span style="color:#006400; font-weight:bold; font-size:0.85em; white-space:nowrap;">Pré-requisito</span>
      </div>
      <div style="display:inline-flex; align-items:center; margin:0 2px;">
        <span style="color:#0056b3; font-weight:bold; margin-right:3px;">■</span>
        <span style="color:#0056b3; font-weight:bold; font-size:0.85em; white-space:nowrap;">Selecionada</span>
      </div>
      <div style="display:inline-flex; align-items:center; margin:0 2px;">
        <span style="color:#b30000; font-weight:bold; margin-right:3px;">■</span>
        <span style="color:#b30000; font-weight:bold; font-size:0.85em; white-space:nowrap;">Trancada diretamente</span>
      </div>
      <div style="display:inline-flex; align-items:center; margin:0 2px;">
        <span style="color:#cc8400; font-weight:bold; margin-right:3px;">■</span>
        <span style="color:#cc8400; font-weight:bold; font-size:0.85em; white-space:nowrap;">Trancada indiretamente</span>
      </div>
    </div>
    """
    st.markdown(legenda_compacta, unsafe_allow_html=True)

# Remover a legenda original que fica abaixo da grade (comentar ou remover esta parte)
# legenda_html = """
# <div style="text-align:center; margin:20px 0; padding:10px;">
#   ...
# </div>
# """
# st.markdown(legenda_html, unsafe_allow_html=True)

# Funções para buscar pré-requisitos
def buscar_pre_requisitos(materia, indireto=False):
    visitados = set()
    fila = [materia]
    resultado = set()

    while fila:
        atual = fila.pop(0)
        for pre in disciplinas[atual]["pre"]:
            if pre not in visitados:
                resultado.add(pre)
                visitados.add(pre)
                if indireto:
                    fila.append(pre)
    return resultado

def buscar_pos_requisitos(materia):
    pos = set()
    for cod, d in disciplinas.items():
        if materia in d["pre"]:
            pos.add(cod)
    return pos

# Modificando a função selecionar_materia para não recarregar a página
def selecionar_materia(cod):
    st.session_state["materia"] = cod
    # Não usamos st.rerun() aqui para evitar o recarregamento

# Verificar se há um parâmetro materia na URL (usando a nova API)
materia_param = st.query_params.get("materia", None)

# Inicializa o estado da matéria selecionada
if "materia" not in st.session_state:
    st.session_state["materia"] = materia_param

# Se temos um parâmetro na URL, atualizamos o estado
if materia_param and materia_param != st.session_state["materia"]:
    st.session_state["materia"] = materia_param
    
# Seleção
materia_sel = st.session_state["materia"]

# CSS para estilizar os elementos clicáveis
st.markdown("""
<style>
    a.materia-item {
        width: 100%;
        border-radius: 6px;
        padding: 5px; /* Reduzido de 8px para 6px */
        margin-bottom: 6px; /* Reduzido de 8px para 6px */
        text-align: center;
        font-weight: bold;
        font-size: 0.85em; /* Adicionando tamanho de fonte reduzido */
        line-height: 1.1    ; /* Ajustando o espaçamento entre linhas */
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        display: block;
        text-decoration: none !important;
        position: relative;
        overflow: hidden;
    }
    
    a.materia-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 0 10px rgba(0,0,0,0.1) inset, 0 0 15px rgba(100,100,255,0.2);
        text-decoration: none !important;
    }
    
    a.materia-item:hover::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
        pointer-events: none;
    }
    
    a.materia-item:active {
        transform: translateY(1px);
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    /* O restante do CSS permanece igual */
    .materia-normal {
        background-color: white;
        color: black !important;
    }
    
    .materia-selecionada {
        background-color: #d0e7ff;
        color: #0056b3 !important;
    }
    
    .materia-pre-requisito {
        background-color: #a8f0a3;
        color: #006400 !important;
    }
    
    .materia-pos-requisito {
        background-color: #ffb3b3;
        color: #b30000 !important;
    }
    
    .materia-pos-indireto {
        background-color: #ffd480;
        color: #cc8400 !important;
    }
    
    div.stButton > button {
        display: none;  /* Esconde os botões do Streamlit */
    }
</style>
""", unsafe_allow_html=True)

# E no loop de renderização, use links diretos com target="_self"
# Layout com colunas por fase - centralizando os títulos
colunas = st.columns(10)
for semestre in range(1, 11):
    with colunas[semestre - 1]:
        # Título centralizado usando HTML
        st.markdown(f"<div style='text-align: center; font-weight: bold; margin-bottom: 8px;'>{semestre}ª Fase</div>", unsafe_allow_html=True)
        
        # Resto do código para as matérias permanece igual
        for cod, dados in disciplinas.items():
            if dados["semestre"] == semestre:
                nome = dados["nome"]
                
                # Definir classe CSS
                classe_css = "materia-normal"
                
                if materia_sel:
                    diretos = buscar_pre_requisitos(materia_sel, indireto=False)
                    pos_diretos = buscar_pos_requisitos(materia_sel)
                    pos_indiretos = set()
                    for pos in pos_diretos:
                        pos_indiretos.update(buscar_pos_requisitos(pos))
                    pos_indiretos = pos_indiretos - pos_diretos
                    
                    if cod == materia_sel:
                        classe_css = "materia-selecionada"
                    elif cod in diretos:
                        classe_css = "materia-pre-requisito"
                    elif cod in pos_diretos:
                        classe_css = "materia-pos-requisito"
                    elif cod in pos_indiretos:
                        classe_css = "materia-pos-indireto"
                
                # Link direto permanece igual
                st.markdown(f"""
                    <a href="?materia={cod}" target="_self" 
                       class="materia-item {classe_css}">
                        {nome}
                    </a>
                """, unsafe_allow_html=True)
                
# Legenda simplificada para evitar problemas de renderização
#st.markdown("<br>", unsafe_allow_html=True)

# Primeira, removemos a legenda antiga
# E então adicionamos uma nova versão mais simples e robusta
legenda_html = """
<div style="text-align:center; margin:20px 0; padding:10px;">
  <div style="display:inline-flex; flex-wrap:wrap; gap:15px; align-items:center; justify-content:center;">
    <span style="font-weight:bold; font-size:0.9em; margin-right:10px;">Legenda:</span>
    <div style="display:inline-flex; align-items:center; margin:0 5px;">
      <span style="color:#006400; font-weight:bold; margin-right:5px;">■</span>
      <span style="color:#006400; font-weight:bold;">Pré-requisito</span>
    </div>
    <div style="display:inline-flex; align-items:center; margin:0 5px;">
      <span style="color:#0056b3; font-weight:bold; margin-right:5px;">■</span>
      <span style="color:#0056b3; font-weight:bold;">Selecionada</span>
    </div>
    <div style="display:inline-flex; align-items:center; margin:0 5px;">
      <span style="color:#b30000; font-weight:bold; margin-right:5px;">■</span>
      <span style="color:#b30000; font-weight:bold;">Trancada diretamente</span>
    </div>
    <div style="display:inline-flex; align-items:center; margin:0 5px;">
      <span style="color:#cc8400; font-weight:bold; margin-right:5px;">■</span>
      <span style="color:#cc8400; font-weight:bold;">Trancada indiretamente</span>
    </div>
  </div>
</div>
"""
st.markdown(legenda_html, unsafe_allow_html=True)

# Após o loop de renderização das colunas e antes da legenda
st.markdown("<br>", unsafe_allow_html=True)  # Espaço após a grade

# Detalhes da matéria selecionada
if materia_sel:
    st.markdown("---")
    # Título centralizado mais simples
    st.markdown("<h4 style='text-align: center; font-size: 1.1em;'>Detalhes da Disciplina</h4>", unsafe_allow_html=True)
    
    # Usando componentes nativos do Streamlit para as informações básicas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.8em;'>Código:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{materia_sel}</p>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.8em;'>Nome:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{disciplinas[materia_sel]['nome']}</p>", unsafe_allow_html=True)
        
    with col3:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.8em;'>Carga Horária:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{disciplinas[materia_sel].get('carga', 0)} horas</p>", unsafe_allow_html=True)
        
    with col4:
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.8em;'>Fase:</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold;'>{disciplinas[materia_sel]['semestre']}ª</p>", unsafe_allow_html=True)
    
    #st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)  # Espaço após os detalhes
    
    # Pré-requisitos e disciplinas habilitadas
    col_pre, col_pos = st.columns(2)
    
    with col_pre:
        # Título com HTML simples
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.9em;'>Pré-requisitos</p>", unsafe_allow_html=True)
        
        prereqs = disciplinas[materia_sel]["pre"]
        if prereqs:
            for pre in prereqs:
                # Verifica se o pré-requisito é uma disciplina ou horas
                if pre in disciplinas:
                    # É uma disciplina regular
                    st.markdown(f"<div style='text-align: center;'><span style='color: #006400;'>▪</span> <b>{disciplinas[pre]['nome']}</b> <small>({pre})</small></div>", unsafe_allow_html=True)
                elif "hs" in pre or "Ob" in pre:
                    # É um requisito de horas ou outro requisito especial
                    st.markdown(f"<div style='text-align: center;'><span style='color: #006400;'>▪</span> <b>{pre}</b> <small>(horas acumuladas)</small></div>", unsafe_allow_html=True)
                else:
                    # Outro tipo de pré-requisito
                    st.markdown(f"<div style='text-align: center;'><span style='color: #006400;'>▪</span> <b>{pre}</b></div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center; font-style: italic; color: #666; font-size: 0.9em;'>Nenhum pré-requisito</p>", unsafe_allow_html=True)
    
    with col_pos:
        # Título com HTML simples
        st.markdown("<p style='text-align: center; font-weight: bold; font-size: 0.9em;'>Habilita as disciplinas</p>", unsafe_allow_html=True)
        
        posreqs = buscar_pos_requisitos(materia_sel)
        if posreqs:
            for pos in posreqs:
                st.markdown(f"<div style='text-align: center;'><span style='color: #b30000;'>▪</span> <b>{disciplinas[pos]['nome']}</b> <small>({pos})</small></div>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align: center; font-style: italic; color: #666; font-size: 0.9em;'>Não habilita outras disciplinas</p>", unsafe_allow_html=True)
    
    st.markdown("---")
