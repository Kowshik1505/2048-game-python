import logic

mat = logic.start_game()

print("\nCurrent Board:")
for row in mat:
    print(row)

while True:

    x = input("\nPress the command (W/A/S/D): ")

    if x in ['W', 'w']:
        mat, flag = logic.move_up(mat)

    elif x in ['S', 's']:
        mat, flag = logic.move_down(mat)

    elif x in ['A', 'a']:
        mat, flag = logic.move_left(mat)

    elif x in ['D', 'd']:
        mat, flag = logic.move_right(mat)

    else:
        print("Invalid Key Pressed")
        continue

    status = logic.get_current_state(mat)

    if status == 'GAME NOT OVER':
        logic.add_new_2(mat)

    print("\nBoard:")
    for row in mat:
        print(row)

    print("\nStatus:", status)

    if status in ['WON', 'LOST']:
        break