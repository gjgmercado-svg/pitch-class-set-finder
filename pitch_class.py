"""
pitch_class.py - Algoritmos para teoría de conjuntos de clases de alturas (Pitch Class Sets)
"""

# Mapeo opcional de nombres de notas a números enteros (0 a 11)
NOTE_MAP = {
    'C': 0, 'B#': 0,
    'C#': 1, 'DB': 1,
    'D': 2,
    'D#': 3, 'EB': 3,
    'E': 4, 'FB': 4,
    'F': 5, 'E#': 5,
    'F#': 6, 'GB': 6,
    'G': 7,
    'G#': 8, 'AB': 8,
    'A': 9,
    'A#': 10, 'BB': 10,
    'B': 11, 'CB': 11
}

def parse_input(input_str):
    """
    Convierte una cadena de texto (notas como 'C E G' o números como '0 4 7')
    en una lista de Pitch Classes enteros [0..11] sin duplicados.
    """
    tokens = input_str.replace(',', ' ').split()
    pc_set = set()
    
    for token in tokens:
        clean_token = token.strip().upper()
        if clean_token in NOTE_MAP:
            pc_set.add(NOTE_MAP[clean_token])
        elif clean_token.isdigit() or (clean_token.startswith('-') and clean_token[1:].isdigit()):
            pc_set.add(int(clean_token) % 12)
        else:
            raise ValueError(f"Entrada no válida: '{token}'")
            
    return sorted(list(pc_set))


def get_normal_form(pc_list):
    """
    Calcula la Forma Normal de un Pitch Class Set.
    """
    if not pc_list:
        return []
        
    n = len(pc_list)
    pcs = sorted(list(set(pc_list)))
    
    if n == 1:
        return pcs

    rotations = []
    for i in range(n):
        rot = pcs[i:] + [x + 12 for x in pcs[:i]]
        rotations.append((rot, pcs[i:] + pcs[:i]))

    # Evaluar la menor amplitud total (último elemento - primer elemento)
    def span(rot_pair):
        r_expanded = rot_pair[0]
        return r_expanded[-1] - r_expanded[0]

    min_span = min(span(r) for r in rotations)
    candidates = [r for r in rotations if span(r) == min_span]

    if len(candidates) == 1:
        return candidates[0][1]

    # En caso de empate, comparar intervalos desde el primer elemento hacia el penúltimo
    for k in range(n - 2, 0, -1):
        def inner_span(rot_pair):
            return rot_pair[0][k] - rot_pair[0][0]
            
        min_inner = min(inner_span(r) for r in candidates)
        candidates = [r for r in candidates if inner_span(r) == min_inner]
        if len(candidates) == 1:
            break

    return candidates[0][1]


def invert_pc_set(pc_list):
    """Invierte el conjunto respecto a 0: T0I(x) = (12 - x) % 12."""
    return sorted(list(set((12 - x) % 12 for x in pc_list)))


def zero_transpose(pc_list):
    """Transpone un conjunto para que comience en 0."""
    if not pc_list:
        return []
    first = pc_list[0]
    return [(x - first) % 12 for x in pc_list]


def get_prime_form(pc_list):
    """
    Calcula la Forma Prima (Prime Form - Forte/Rahn) del conjunto.
    1. Calcula Normal Form.
    2. Transpone a 0.
    3. Invierte, obtiene Normal Form de la inversión y transpone a 0.
    4. Compara ambas y elige la más "empacada hacia la izquierda".
    """
    if not pc_list:
        return []

    nf = get_normal_form(pc_list)
    nf_zero = zero_transpose(nf)

    inv = invert_pc_set(pc_list)
    inf_nf = get_normal_form(inv)
    inf_zero = zero_transpose(inf_nf)

    # Comparación léxica de derecha a izquierda o de izquierda a derecha (Algoritmo Forte/Rahn)
    for a, b in zip(nf_zero, inf_zero):
        if a < b:
            return nf_zero
        elif b < a:
            return inf_zero

    return nf_zero


def get_interval_vector(pc_list):
    """
    Calcula el Vector de Intervalos (ICV - Interval Class Vector) de 6 dígitos.
    Mide la presencia de las clases de intervalo 1 a 6.
    """
    pcs = sorted(list(set(pc_list)))
    vector = [0] * 6
    n = len(pcs)
    
    for i in range(n):
        for j in range(i + 1, n):
            diff = abs(pcs[i] - pcs[j]) % 12
            ic = min(diff, 12 - diff)
            if 1 <= ic <= 6:
                vector[ic - 1] += 1
                
    return vector
