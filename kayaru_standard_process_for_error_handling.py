import kayaru_standard_process  as kstd
import kayaru_standard_messages as kstd_m

def assertion_check(result,message):
    assert result,message

def assertion_check_is_int(var,var_name=""):
    result = kstd.is_int(var)
    if not ( result ):
        name    = kstd.get_var_name(var)
        if var_name != "":
            message = kstd_m.get_X_is_not_int(var_name)
        else:
            message = kstd_m.get_X_is_not_int("X")
        assertion_check(result,message)

