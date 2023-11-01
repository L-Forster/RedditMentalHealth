from enum import Enum
#Template:
class Sort(Enum):
    NEW = "new"
    HOT = "hot"
    TOP = "top"

class SubNames(Enum):
    DEPR = "depression"
    SCHZ = "schizophrenia"
    NAR = "npd"
    ADHD = "adhd"
    BIP = "bipolar"
    AUT = "autism"
    ASPD = "aspd"
    CAS = "casualconversation"



# Example:
# thisdict = {
#     "id": SubNames.EXAMPLE,
#     "flair": ["flair a", "flair b", "flair c"],
#     "filters": Sort.NEW
# }

class SubData():
    def __init__(self, name, flair, filters, time):
        self.name = name
        self.flair = flair
        self.filters = filters
        self.time = time

    def getId(self):
        return self.name

    def getFlair(self):
        return self.flair

def instantiateNewDisorder(enumId, flairs):
    disorder = {
        "id": enumId,
        "flair": flairs,
        "filters": Sort.TOP
    }
    return disorder
def initDict():

    global depr
    global schz
    global nar
    global adhd
    global bip
    global aut
    global aspd

    disorders = []

    depr = {
        "id": SubNames.DEPR,
        "flair": ["null"],
        "filters": Sort.TOP,
        "time_limit": "month"
    }
    disorders.append(depr)

    schz = {
        "id": SubNames.SCHZ,
        "flair": ["Seeking Support", "Trigger Warning", "Hallucinations / Delusions"],
        "filters": Sort.TOP,
        "time_limit": "year"
    }
    disorders.append(schz)

    nar = {
        "id": SubNames.NAR,
        "flair": ["null"],
        "filters": Sort.TOP,
        "time_limit": "month"
    }
    disorders.append(nar)

    adhd = {
        "id": SubNames.ADHD,
        "flair": ["null"],
        "filters": Sort.TOP,
        "time_limit": "month"
    }
    disorders.append(adhd)

    bip = {
        "id": SubNames.BIP,
        "flair": ["Support/Advice :shy:"],
        "filters": Sort.NEW,
        "time_limit": "month"
    }
    disorders.append(bip)

    aut = {
        "id": SubNames.AUT,
        "flair": ["Rant/Vent", "Discussion", "Question", "Advice"],
        "filters": Sort.TOP,
        "time_limit": "month"
    }
    disorders.append(aut)

    ## This one should also take post comments (as well as post body)

    aspd = {
        "id": SubNames.ASPD,
        "flair": ["Rant", "Discussion"],
        "filters": Sort.TOP,
        "time_limit": "year"
    }
    disorders.append(aspd)

    whol = {
        "id": SubNames.CAS,
        "flair": ["null"],
        "filters": Sort.TOP,
        "time_limit": "month"
    }
    disorders.append(whol)

    return disorders



def createSub(strName):
    # Turn the name into enum
    sub_dict = initDict()
    sub_info = []
    # list of dictionaries
    # if strName == "narcissism":
    #     strName = SubNames.NAR

    try:
        enum_value = SubNames(strName)
    except:
        print("No corresponding Enum class\n")
        enum_value = "null"
        raise ValueError("!!!")
    # Get data from corresponding dict
    for sub in sub_dict:
        if sub["id"] == enum_value:
            sub_info = sub
            break

    my_sub_data = SubData(sub_info["id"], sub_info["flair"], sub_info["filters"], sub_info["time_limit"])


    return my_sub_data

