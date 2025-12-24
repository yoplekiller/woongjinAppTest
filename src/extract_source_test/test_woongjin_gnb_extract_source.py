from utils.gnb_page_source_helper import save_gnb_source, print_gnb_elements

def test_gnb(home_page):
    # GNB 소스만 저장
    save_gnb_source(home_page.driver, "gnb_only.xml")
    
    # GNB 요소 출력
    print_gnb_elements(home_page.driver)