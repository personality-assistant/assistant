width = 5
for num in range(12):
    print('{:^10} {:^10} {:^10}'.format(num, num**2, num**3))



# CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
# TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
#                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
#
# TRANS = {}
# for c, i in zip(CYRILLIC_SYMBOLS, TRANSLATION):
#     TRANS[ord(c)] = i
#     TRANS[ord(c.upper())] = i.upper()
# print(TRANS)
#
#
# def translate(name):
#     return name.translate(TRANS)

#
# print(translate('ЧАША'))





















# def is_spam_words(text, spam_words, space_around=False):
#     if space_around:
#         text_list = text.replace(' ', '.').split('.')
#         spam_words = [i.lower() for i in spam_words]
#         result = set(spam_words) & set(text_list)
#         return bool(result)
#
#     else:
#         spam_words = [i.lower() for i in spam_words]
#         for word in spam_words:
#             if word in text.lower():
#                 return True
#         return False
#
#
# print(is_spam_words('эNот петух Bоlьше нам не друг молох.', ['лох', 'бараН', 'шершень']))


