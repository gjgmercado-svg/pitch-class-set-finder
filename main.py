"""
main.py - CLI para interactuar con el Pitch Class Set Finder
"""
from pitch_class import (
    parse_input,
    get_normal_form,
    get_prime_form,
    get_interval_vector
)

def format_set(pc_list):
    return "(" + " ".join(str(x) for x in pc_list) + ")"

def format_vector(vec):
    return "<" + "".join(str(x) for x in vec) + ">"

def main():
    print("=" * 55)
    print("      PITCH CLASS SET FINDER & CALCULATOR")
    print("=" * 55)
    print("Ingresa las notas o números separados por espacios.")
    print("Ejemplos válidos:")
    print("  - Notas:  C E G")
    print("  - Notas:  C# D D# G")
    print("  - Enteros: 0 4 7 11")
    print("Escribe 'salir' para terminar.\n")

    while True:
        try:
            user_input = input("Entrada > ").strip()
            if user_input.lower() in ['salir', 'exit', 'q']:
                print("¡Hasta luego!")
                break
                
            if not user_input:
                continue

            pcs = parse_input(user_input)
            nf = get_normal_form(pcs)
            pf = get_prime_form(pcs)
            icv = get_interval_vector(pcs)

            print("\n--- RESULTADOS ---")
            print(f" Pitch Class Set:  {format_set(pcs)}")
            print(f" Normal Form:      {format_set(nf)}")
            print(f" Prime Form:       ({','.join(str(x) for x in pf)})")
            print(f" Interval Vector:  {format_vector(icv)}")
            print("-" * 25 + "\n")

        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}\n")

if __name__ == "__main__":
    main()
