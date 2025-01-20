
"""
İmplementasyonun test sistemi ile uyumlu olmasi için aşağıdaki fonksiyonlar formatiyla implementasyonda olmali 

util import edilmeli
"""

# Takes mk and returns round keys as 2d list
def key_schedule(key):
    
    return [expanded_keys[i:i + 16] for i in range(0, len(expanded_keys), 16)]