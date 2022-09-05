def elimina_nulos(d):
    limpo = {}
    for k, v in d.items():
        print(' ', d.items())
        if isinstance(v, dict):
            nested = elimina_nulos(v)
            print('lara',nested)
            if len(nested.keys()) > 0:
                limpo[k] = nested
                print('oi',limpo[k])
        elif v is not None:
            limpo[k] = v
            print('mariana',limpo[k])
        print('value  ',v, '    key  ',k)
    return limpo


dic={1:{2:
        {3:4}}
    ,0:{}
    }
print(elimina_nulos(dic))

