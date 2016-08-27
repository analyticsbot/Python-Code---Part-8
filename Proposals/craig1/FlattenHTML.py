from html.parser import HTMLParser


class HTMLMark:    
  def is_open(self):
    return False

  def is_tag(self):
    return False

  def is_data(self):
    return False


class DataMark(HTMLMark):
  def __init__(self, data):
    self.data = data
    super(HTMLMark, self).__init__()

  def __str__(self):
    return "<DATA> <DATA " + self.data + ">" 

  def is_data(self):
    return True

  def get_data(self):
    return self.data


class TagMark(HTMLMark):
  def __init__(self, tag):
    self.tag = tag
    super(HTMLMark, self).__init__()

  def get_tag(self):
    return self.tag

  def is_tag(self):
    return True


class OpenTagMark(TagMark):
  def __init__(self, tag, attrs):
    self.attrs = dict(attrs)
    super(OpenTagMark, self).__init__(tag)

  def __str__(self):
    return "<OPEN> <TAG " + self.tag  + "> <ATTRS " + str(self.attrs) + ">" 

  def is_open(self):
    return True

  def get_attr(self, key):
    if key in self.attrs:
      return self.attrs[key]
    else:
      return None

class CloseTagMark(TagMark):
  def __init__(self, tag):
    super(CloseTagMark, self).__init__(tag)

  def __str__(self):
    return "<CLOSE> <TAG " + self.tag + ">" 


class MarksCollector(HTMLParser):
    def __init__(self):
      self.marks = []
      super(MarksCollector, self).__init__(convert_charrefs=True)

    def handle_starttag(self, tag, attrs):
      self.marks.append(OpenTagMark(tag, attrs))

    def handle_endtag(self, tag):
      self.marks.append(CloseTagMark(tag))

    def handle_data(self, data):
      self.marks.append(DataMark(data))

    @staticmethod
    def get_open_tags(text):
      collector = MarksCollector()
      collector.feed(text)
      return [e for e in collector.marks if e.is_open()]

    @staticmethod
    def get_ref_tags(text):
      collector = MarksCollector()
      collector.feed(text)
      return [e for e in collector.marks if e.is_open() and e.get_tag() == 'a']

    @staticmethod
    def get_all(text):
      collector = MarksCollector()
      collector.feed(text)
      return collector.marks

def find_tags(marks):
  return find_vals(marks, lambda x: x.is_tag())

def find_indexes(marks, predicate):
  return [i for i, x in enumerate(marks) if predicate(x)]
  
def find_vals(marks, predicate):
  return [x for x in marks if predicate(x)]

