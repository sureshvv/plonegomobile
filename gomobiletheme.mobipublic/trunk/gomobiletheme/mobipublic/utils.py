def shorten_description(desc):
    """ """
    
    if not desc:
        return desc
    
    if len(desc) > 140:
        desc = desc[0:140] + "..."
        
    return desc
