from xml.dom.minidom import getDOMImplementation, parseString


def dict_to_doc(dictionary, attrs=None):
    assert len(dictionary) == 1
    implementation = getDOMImplementation()
    doc = implementation.createDocument(None, dictionary.keys()[0], None)

    def dict_to_nodelist(dictionary, parent):
        for key, child in dictionary.iteritems():
            new = doc.createElement(key)
            parent.appendChild(new)
            if type(child) == dict:
                dict_to_nodelist(child, new)
            else:
                new.appendChild(doc.createTextNode(child))

    if attrs:
        for key, val in attrs.iteritems():
            doc.documentElement.setAttribute(key, val)

    dict_to_nodelist(dictionary.values()[0], doc.documentElement)
    return doc


def doc_to_dict(document):
    first = document.childNodes[0]
    if len(document.childNodes) == 1 and first.nodeName == "#text":
        return first.data
    else:
        return dict(
            (child.nodeName, doc_to_dict(child))
            for child in document.childNodes
            if child.nodeName != '#text' or child.data.strip() != ''
        )


def dict_to_xml(dictionary, attrs=None):
    return dict_to_doc(dictionary, attrs).toxml()


def xml_to_dict(xml_string):
    return doc_to_dict(parseString(xml_string))
