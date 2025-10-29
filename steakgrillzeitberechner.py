# Der Steakgrillzeitberechner

times = [
    {1: 1, 2: 2, 3: 4, 4: 6},
    {1: 1, 2: 3, 3: 5, 4: 7},
    {1: 1, 2: 4, 3: 8, 4: 10},
    {1: 1, 2: 5, 3: 10, 4: 12},
]


def main():
    try:
        dim = float(input("Wie dick ist dein Steak? (in cm)\n> "))
    except ValueError:
        print("Ungültige Eingabe!")
        return

    if dim > 5:
        print("Dein Steak ist viel zu dick!")
        return
    if dim < 1:
        print("Aufschnitt!")
        return

    print("Sehr schön!")
    try:
        grade = int(input("Wähle deine Garstufe! (1-4)\n> "))
    except ValueError:
        print("Ungültige Eingabe!")
        return

    if grade < 1 or grade > 4:
        print("Keine gültige Garstufe!")
        return

    # Determine grill time
    if dim <= 2:
        t = times[0][grade]
    elif dim <= 2.5:
        t = times[1][grade]
    elif dim <= 3:
        t = times[2][grade]
    elif dim <= 5:
        t = times[3][grade]
    else:
        print("Dimension nicht unterstützt.")
        return

    print(f"Grille dein Steak {t / 2:.1f} Minuten von jeder Seite!")


if __name__ == "__main__":
    main()
