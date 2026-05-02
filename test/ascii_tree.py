
import random

def generate_ascii_tree(height=random.randint(8, 18)):
    tree = []
    # Crown
    # Make the crown wider and less pointy, resembling a deciduous tree
    for i in range(height):
        # Create a more rounded or bushy crown shape
        # The widest part will be around the middle of the crown's visible height
        # It will start narrow, get wider, then get narrower again
        current_width = 0
        if i < height // 2:
            current_width = 1 + (2 * i)
        else:
            current_width = 1 + (2 * (height - i - 1))

        # Add some randomness to the width to make it less perfect
        current_width += random.randint(-1, 1) * 2
        if current_width < 3: current_width = 3 # Minimum width

        indent = " " * (height - (current_width // 2) - 1)
        leaves = random.choice(['@', 'o', '&', '#']) # Deciduous leaf characters
        leaf_row = ""
        for _ in range(current_width):
            leaf_row += leaves + random.choice(["", " "]) # Vary spacing
        tree.append(indent + leaf_row.strip())

    # Branches (simpler representation)
    # Add a couple of lines with '/' and '' to represent main branches below the crown
    num_branch_layers = random.randint(1, 3)
    for _ in range(num_branch_layers):
        branch_indent_offset = random.randint(1, 4)
        branch_length = random.randint(3, 7)
        left_branch = "/" + "_" * random.randint(0,2)
        right_branch = "_" * random.randint(0,2) + "\\"
        middle_trunk_part = "|" * random.randint(1,2)

        total_branch_line_width = len(left_branch) + len(middle_trunk_part) + len(right_branch)
        indent_for_branch_line = " " * (height - (total_branch_line_width // 2) - 1 - random.randint(-1,1))
        tree.append(indent_for_branch_line + left_branch + middle_trunk_part + right_branch)


    # Trunk
    trunk_height = random.randint(height // 4, height // 3)
    trunk_width = random.randint(2, 4)
    for _ in range(trunk_height):
        # Slightly vary trunk position for a more natural look
        trunk_indent_offset = random.randint(-1, 1)
        indent = " " * (height - (trunk_width // 2) - 1 + trunk_indent_offset)
        trunk_char = random.choice(['|', 'I', 'Y'])
        tree.append(indent + trunk_char * trunk_width)

    return "\n".join(tree)

if __name__ == "__main__":
    print(generate_ascii_tree())
