# Blog

<!-- Overriding custom style that hides the sidebar,
     because we want it for the blog
-->
<style>
.md-sidebar--primary {
  display: block;
}
.md-main__inner {
  flex-direction: row;
}

ul.md-nav__list{
  flex-direction: column;

}
@media only screen and (max-width: 60em) {

.md-main__inner {
    flex-direction: column;
    margin: 0 5vw;
    .md-content {
      margin: 0;
    }
  }
}
</style>