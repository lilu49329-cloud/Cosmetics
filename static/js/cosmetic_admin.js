document.addEventListener('DOMContentLoaded', function() {
    // Ép Sidebar sang màu sáng bằng cách xóa class dark
    const sidebar = document.querySelector('aside.main-sidebar');
    if (sidebar) {
        sidebar.classList.remove('sidebar-dark-primary', 'sidebar-dark-pink', 'sidebar-dark-info');
        sidebar.classList.add('sidebar-light-primary');
        // Ép màu trắng trực tiếp bằng style
        sidebar.style.backgroundColor = '#ffffff';
    }
    
    // Khử cái bóng mờ và hộp trắng ở phần Logo & Admin
    const elementsToClear = document.querySelectorAll('.brand-link, .brand-image, .user-panel, .info, .nav-header');
    elementsToClear.forEach(el => {
        el.style.backgroundColor = 'transparent';
        el.style.boxShadow = 'none';
        el.style.border = 'none';
    });
    
    const brandLink = document.querySelector('.brand-link');
    if (brandLink) {
        brandLink.style.borderBottom = '1px solid #ffe6f0';
    }
});
