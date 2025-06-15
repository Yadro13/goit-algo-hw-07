class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    # Метод для виводу дерева (старий стиль — вертикальний)
    def __str__(self):
        return self._str_tree()

    def _str_tree(self, prefix="", is_tail=True):
        ret = prefix + ("└── " if is_tail else "├── ") + str(self.key) + "\n"
        if self.left and self.right:
            ret += self.left._str_tree(prefix + ("    " if is_tail else "│   "), False)
            ret += self.right._str_tree(prefix + ("    " if is_tail else "│   "), True)
        elif self.left:
            ret += self.left._str_tree(prefix + ("    " if is_tail else "│   "), True)
        elif self.right:
            ret += self.right._str_tree(prefix + ("    " if is_tail else "│   "), True)
        return ret


# Допоміжні функції
def get_height(node):
    if not node:
        return 0
    return node.height

def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)

# Повороти для підтримки балансу
def left_rotate(z):
    y = z.right
    T2 = y.left

    y.left = z
    z.right = T2

    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))

    return y

def right_rotate(y):
    x = y.left
    T3 = x.right

    x.right = y
    y.left = T3

    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))

    return x

def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

# Вставка нового вузла
def insert(root, key):
    if not root:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root  # Значення вже є

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    # Балансування
    if balance > 1 and key < root.left.key:
        return right_rotate(root)
    if balance < -1 and key > root.right.key:
        return left_rotate(root)
    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

# Видалення вузла
def delete_node(root, key):
    if not root:
        return root

    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp

        temp = min_value_node(root.right)
        root.key = temp.key
        root.right = delete_node(root.right, temp.key)

    if root is None:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    # Балансування
    if balance > 1 and get_balance(root.left) >= 0:
        return right_rotate(root)
    if balance > 1 and get_balance(root.left) < 0:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    if balance < -1 and get_balance(root.right) <= 0:
        return left_rotate(root)
    if balance < -1 and get_balance(root.right) > 0:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

# Функція для знаходження найбільшого значення в дереві
def find_max(root):
    if not root:
        return None
    current = root
    while current.right:
        current = current.right
    return current.key

# Функція для знаходження найменшого значення в дереві
def find_min(root):
    if not root:
        return None
    current = root
    while current.left:
        current = current.left
    return current.key

# Функція для обчислення суми всіх значень у AVL-дереві
def sum_tree(root):
    if not root:
        return 0
    return root.key + sum_tree(root.left) + sum_tree(root.right)

# Візуалізація дерева горизонтально з гілками
def build_ascii_tree(node):

    if node is None:
        return [], 0, 0, 0

    node_repr = str(node.key)
    new_root_width = len(node_repr)

    # Побудова лівого та правого піддерев
    l_lines, l_width, l_height, l_middle = build_ascii_tree(node.left)
    r_lines, r_width, r_height, r_middle = build_ascii_tree(node.right)

    # Ширина між піддеревами
    gap_size = 2
    line1 = " " * l_middle + " " * (l_width - l_middle) + node_repr + " " * r_width
    line2 = ""

    # Гілка вліво
    if node.left:
        left_branch = " " * l_middle + "/" + " " * (l_width - l_middle - 1 + new_root_width)
    else:
        left_branch = " " * (l_width + new_root_width)

    # Гілка вправо
    if node.right:
        right_branch = " " * r_middle + "\\" + " " * (r_width - r_middle - 1)
    else:
        right_branch = " " * r_width

    line2 = left_branch + right_branch

    # Вирівнювання висоти піддерев
    height = max(l_height, r_height)
    l_lines += [" " * l_width] * (height - l_height)
    r_lines += [" " * r_width] * (height - r_height)

    # Об’єднання піддерев
    merged_lines = [
        l + " " * new_root_width + r
        for l, r in zip(l_lines, r_lines)
    ]

    return [line1, line2] + merged_lines, l_width + new_root_width + r_width, height + 2, l_width + new_root_width // 2



# Тестування
if __name__ == "__main__":
    root = None
    keys = [10, 20, 30, 25, 28, 27, -1, 15, 5, 3, 8, 12, 18, 22, 35, 40, 50, 45, 60, 70, 65, 55, 75]

    for key in keys:
        root = insert(root, key)
        print("Вставлено:", key)

    keys_to_delete = [10, 27]
    for key in keys_to_delete:
        root = delete_node(root, key)
        print("Видалено:", key)
        print("AVL-Дерево:")
        print(root)

    print("----------------------------------------------------")
    print("Найбільше значення в AVL-дереві:", find_max(root))
    print("----------------------------------------------------")
    print("Найменше значення в AVL-дереві:", find_min(root))
    print("----------------------------------------------------")
    print("Сума всіх значень у дереві:", sum_tree(root))
    print("----------------------------------------------------")
    print("Горизонтальне відображення дерева:")

    lines, *_ = build_ascii_tree(root)
    print()
    print("\n".join(lines))
