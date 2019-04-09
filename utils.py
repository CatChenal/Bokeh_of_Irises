# -*- coding: utf-8 -*-
# utils

AS_OF = 'April 2019'


def is_lab_notebook():
    import re
    import psutil
        
    return any(re.search('jupyter-lab-script', x)
                    for x in psutil.Process().parent().cmdline())


def check_notebook():
    if is_lab_notebook():
        # need to use Markdown if referencing variables:
        from IPython.display import Markdown
        msg = "#### This is a <span style=\"color:red;\">JupyterLab notebook \
              </span>: Use `IPython.display.Markdown()` if referencing variables; \
              {{var}} does not work."
        return Markdown(msg)


def get_html_tpl(tpl_fullname):
    """ This uses FileSystemLoader (FSL), not PackageLoader.
        Assumes dir for FSL is tpl_fullname parent dir.
    """
    import os
    from jinja2 import Environment, FileSystemLoader
    
    tpl_dir = os.path.dirname(tpl_fullname)
    tpl_name = os.path.basename(tpl_fullname)
    
    jenv = Environment(loader=FileSystemLoader(tpl_dir), trim_blocks=True)
    return jenv.get_template(tpl_name)


def save_file(outname, ext, s, replace=True):
    import os
    
    # check if outname has an extension
    try:
        i = outname.index('.' , -6)
        outfile = outname[:i] + '.' + ext
    except:
        outfile = outname + '.' + ext
    
    if replace:
        if os.path.exists(outfile):
            os.remove(outfile)

    if isinstance(s, dict):
        import json
        
        with open(outfile, 'w') as f:
            f.write(json.dumps(s))
    else:
        if len(s):
            with open(outfile, 'w') as f:
                f.write(s)
    return


def caveat_codor():
    import sys
    from IPython.display import Markdown

    mysys = '{} | {}<br>As of:  {}'.format(sys.version,
                                           sys.platform,
                                           str(AS_OF))
    msg = "The code and information herein is valid given my "
    msg += "understanding and this environment:<br>"
    return Markdown(msg + mysys)

    

def format_with_bold(s_format, f_id = 'b'):
    """
    Returns the string with all placeholders preceeded by '_b' replaced 
    with a bold indicator value;
    
    :param: s_format: a string format; 
            if contains '_b{}b_' this term gets bolded.
    :TODO:  implement framed or circled
    
    :param: s: a string or value
    
    Note 1: '... _b{}; something {}b_ ...' is a valid format.
    Note 2: IndexError is raised using the output format only when
            the input tuple length < number of placeholders ({});
            it is silent when the later are greater (see Example).
    
    Example:
    # No error:
    fmt = 'What! _b{}b_; yes: _b{}b_; no: {}.'
    print(format_with_bold(fmt).format('Cat', 'dog', 3, '@no000'))
    # IndexError:
    print(format_with_bold(fmt).format('Cat', 'dog'))
    """
    #frmt_id = 'b' #: for bold
    frmt_id = f_id
    
    # for err msg:
    expect = "Expected: _{0}{{}}{0}_".format(frmt_id)
    
    x1 = '_'+frmt_id
    x0 = frmt_id+'_'
    
    # Check for paired markers:
    if s_format.count(x1) != s_format.count(x0):
        err_msg1 = "Indicators not paired. " + expect
        raise LookupError(err_msg1)
    
    # Check for start  marker:
    i = s_format.find(x1 + '{')
    
    # Check marker order:
    if i > s_format.find('}' + x0):
        err_msg2 = "Starting indicator not found. " + expect
        raise LookupError(err_msg2)
        
    while i != -1:
        #s_format = s_format.replace(x1, '\033[1m')
        
        # Check for trailing bold marker:
        j = s_format.find('}' + x0)
        
        if j != -1:
            if frmt_id == 'b':
                s_format = s_format.replace(x1, '\033[1m')
                s_format = s_format.replace(x0, '\033[0m')
            elif frmt_id == 'f':
                # not correct:
                s_format = s_format.replace(x1, '\033[51m')
                s_format = s_format.replace(x0, '\033[54m')
        else:
            err_msg3 = "Trailing bold indicator not found. " + expect
            raise LookupError(err_msg3)
            
        i = s_format.find(x1 + '{')
    
    return s_format