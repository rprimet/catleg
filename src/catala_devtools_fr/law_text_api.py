"""
Current OCaml API


val get_article_id : article -> string
val get_article_text : article -> string
val get_article_title : article -> string
val get_article_expiration_date : article -> Unix.tm
val get_article_new_version : article -> string

"""
from datetime import date
from typing import Protocol

class Article(Protocol):
  @property
  def id(self) -> str:
      """
      """
      pass

  @property
  def text(self) -> str:
      """
      """
      pass
  
  @property
  def expiration_date(self) -> date:
      """
      """
      pass
  
  @property
  def new_version(self) -> str:
      """
      """
      pass