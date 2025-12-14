def calculate_minrun(size):
    remainder = 0
    while size >= 16:
        remainder |= size & 1
        size >>= 1
    return size + remainder

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    result_position = right
    while left <= right:
        middle = left + (right - left) // 2
        if abs(arr[middle]) < abs(target):
            result_position = middle - 1
            right = middle - 1
        else:
            left = middle + 1
    return result_position

def merge_with_gallop(left_array, right_array, merge_index):
    merged_result = []
    left_index, right_index = 0, 0
    left_gallop_count = 0
    right_gallop_count = 0
    total_gallops = 0

    while left_index < len(left_array) and right_index < len(right_array):
        if abs(left_array[left_index]) >= abs(right_array[right_index]):
            merged_result.append(left_array[left_index])
            left_index += 1
            left_gallop_count += 1
            right_gallop_count = 0

            if left_gallop_count >= 3:
                gallop_end_index = binary_search(left_array[left_index:], right_array[right_index]) + left_index
                total_gallops += 1
                while left_index <= gallop_end_index:
                    merged_result.append(left_array[left_index])
                    left_index += 1
                left_gallop_count = 0
        else:
            merged_result.append(right_array[right_index])
            right_index += 1
            right_gallop_count += 1
            left_gallop_count = 0

            if right_gallop_count >= 3:
                gallop_end_index = binary_search(right_array[right_index:], left_array[left_index]) + right_index
                total_gallops += 1
                while right_index <= gallop_end_index:
                    merged_result.append(right_array[right_index])
                    right_index += 1
                right_gallop_count = 0

    merged_result.extend(left_array[left_index:])
    merged_result.extend(right_array[right_index:])

    print(f"Gallops {merge_index}: {total_gallops}")
    print(f"Merge {merge_index}:", *merged_result)

    return merged_result

def merge_stack(sorted_blocks):
    stack = []
    merge_step = 0

    for block in sorted_blocks:
        stack.append(block)

        while len(stack) >= 2:
            if len(stack) == 2:
                right_block = stack.pop()
                left_block = stack.pop()

                if len(left_block) <= len(right_block):
                    merged_block = merge_with_gallop(left_block, right_block, merge_step)
                    merge_step += 1
                    stack.append(merged_block)
                else:
                    stack.append(left_block)
                    stack.append(right_block)
                    break

            if len(stack) > 2:
                right_block = stack.pop()
                middle_block = stack.pop()
                left_block = stack.pop()

                if len(left_block) <= len(right_block) + len(middle_block) or len(middle_block) <= len(right_block):
                    if max(len(right_block), len(left_block)) == len(left_block):
                        merged_block = merge_with_gallop(middle_block, right_block, merge_step)
                        merge_step += 1
                        stack.append(left_block)
                        stack.append(merged_block)
                    else:
                        merged_block = merge_with_gallop(middle_block, left_block, merge_step)
                        merge_step += 1
                        stack.append(merged_block)
                        stack.append(right_block)
                else:
                    stack.append(left_block)
                    stack.append(middle_block)
                    stack.append(right_block)
                    break

    while len(stack) > 1:
        if len(stack) == 2:
            right_block = stack.pop()
            left_block = stack.pop()
            merged_block = merge_with_gallop(left_block, right_block, merge_step)
            merge_step += 1
            stack.append(merged_block)

        if len(stack) > 2:
            right_block = stack.pop()
            middle_block = stack.pop()
            left_block = stack.pop()

            if max(len(right_block), len(left_block)) == len(left_block):
                merged_block = merge_with_gallop(middle_block, right_block, merge_step)
                merge_step += 1
                stack.append(left_block)
                stack.append(merged_block)
            else:
                merged_block = merge_with_gallop(middle_block, left_block, merge_step)
                merge_step += 1
                stack.append(merged_block)
                stack.append(right_block)

    return stack.pop()

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and abs(key) > abs(arr[j]):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def timsort(arr, n):
    minrun = calculate_minrun(n)
    current_block = []
    sorted_blocks = []
    block_index = 0
    is_increasing = is_decreasing = True
    i = 0

    while i < n:
        while i < n - 1 and abs(arr[i]) < abs(arr[i + 1]) and is_increasing:
            current_block.append(arr[i])
            is_decreasing = False
            i += 1
        while i < n - 1 and abs(arr[i]) >= abs(arr[i + 1]) and is_decreasing:
            current_block.append(arr[i])
            is_increasing = False
            i += 1
        current_block.append(arr[i])

        if is_increasing:
            current_block.reverse()

        while i < n - 1 and len(current_block) < minrun:
            i += 1
            current_block.append(arr[i])

        insertion_sort(current_block)
        sorted_blocks.append(current_block)
        print(f"Part {block_index}:", *current_block)

        current_block = []
        is_increasing = is_decreasing = True
        i += 1
        block_index += 1

    if len(sorted_blocks) > 1:
        result = merge_stack(sorted_blocks)
    else:
        result = sorted_blocks.pop()

    return result

# Чтение ввода и запуск
n = int(input())
arr = list(map(int, input().split()))
print("Answer:", *timsort(arr, n))
