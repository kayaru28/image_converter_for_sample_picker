import kayaru_standard_process  as kstd
import kayaru_standard_messages as kstd_m

def assertionCheck(result,message):
    assert result,message

def assertionCheckIsInt(var,var_name=""):
    result = kstd.isInt(var)
    if not ( result ):
        name    = kstd.getVarName(var)
        if var_name != "":
            message = kstd_m.get_XIs_not_int(var_name)
        else:
            message = kstd_m.get_XIs_not_int(name)
        assertionCheck(result,message)

def assertionCheckIsStr(var,var_name=""):
    result = kstd.isStr(var)
    if not ( result ):
        name    = kstd.getVarName(var)
        if var_name != "":
            message = kstd_m.get_XIs_not_str(var_name)
        else:
            message = kstd_m.get_XIs_not_int(name)
        assertionCheck(result,message)

def assertionCheckIsList(var,var_name=""):
    result = kstd.isList(var)
    if not ( result ):
        name    = kstd.getVarName(var)
        if var_name != "":
            message = kstd_m.get_XIs_not_list(var_name)
        else:
            message = kstd_m.get_XIs_not_int(name)
        assertionCheck(result,message)


