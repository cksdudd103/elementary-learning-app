from app.services.math_generator import generate_math_set

items = generate_math_set(6, 30)
print('count', len(items))
print(items[0])
print(items[-1])
