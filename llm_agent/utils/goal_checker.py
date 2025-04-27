def goal_checker(elements, constraints):
    result = {key: False for key in constraints}
    found = {}

    for el in elements:
        el_text = str(el.get("text", "")).strip().lower()

        for key, expected in constraints.items():
            expected = str(expected).strip().lower()

            def check_range(value_str, constraint_str):
                if 'between' in constraint_str:
                    low, high = map(float, constraint_str.replace('"','').split('between ')[1].split(' and '))
                    return low <= float(value_str) <= high
                return False

            if key == "screen" and "screen" in el_text:
                try:
                    # Try extracting the first number (e.g., 13.3" Screen)
                    screen_val = float(el_text.split('"')[0])
                    if check_range(str(screen_val), expected):
                        result[key] = True
                        found[key] = el_text
                except ValueError:
                    continue

            elif key == "battery" and "battery" in el_text:
                try:
                    battery_hours = float(el_text.split()[0])
                    if 'at least' in expected:
                        threshold = float(expected.replace('at least', '').split()[0])
                        result[key] = battery_hours >= threshold
                        found[key] = el_text
                except ValueError:
                    continue

            elif key == "price" and "product-price" in el_text:
                try:
                    price = float(el_text.replace("$", "").replace(",", "").split()[0])
                    if 'under' in expected:
                        threshold = float(expected.replace('under', '').replace('$', ''))
                        result[key] = price < threshold
                        found[key] = el_text
                except ValueError:
                    continue

    all_constraints_met = all(result.values())
    if all_constraints_met:
        print(f"✅ All constraints are satisfied.")
        return True, {key: found.get(key, "unknown") for key in constraints}
    else:
        print(f"❌ Some constraints failed: {result}")
        return False, {}
