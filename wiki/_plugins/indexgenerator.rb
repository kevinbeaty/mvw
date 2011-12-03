module Jekyll
    class IndexNode
        attr_accessor :parent, :name, :path, :children, :pages, :indexpage
        attr_writer :indexpage # Generated
        
        def initialize(parent, name)
            @parent = parent
            @name = name
            @pages = []
            @children = []

            parent.children << self unless parent.nil?

            # build path
            up = []

            n = self
            until n.nil?
                up << n.name
                n = n.parent
            end

            @path = File.join(*up.reverse)
        end
    end

    class IndexPage < Page
        def initialize(site, node)
            @site = site
            @base = site.source
            @dir = node.path
            @name = 'index.html'

            # index pages are created depth first, save to map children below 
            node.indexpage = self

            self.process(@name)
            self.read_yaml(File.join(@base, '_layouts'), 'index.html')
            self.data['title'] = node.name
            self.data['pages'] = node.pages
            self.data['children'] = node.children.map { |c| c.indexpage }
        end
    end

    class IndexGenerator < Generator
        safe true

        def generate(site)
            if site.layouts.key? 'index'
                root = IndexNode.new(nil, '')
                site.pages.each do |page|
                   add_to_node_list page, root
                end
                write_index site, root
            end
        end
        
        def add_to_node_list(page, node)
            url = page.to_liquid['url']
            File.dirname(url).split('/').reject {|p| p.eql? ''}.each do |p|
                idx = node.children.index { |child| child.name.eql? p } 
                if idx.nil?
                    node = IndexNode.new(node, p)
                else
                    node = node.children[idx] 
                end
            end
            node.pages << page
        end

        def write_index(site, node)
            # Depth first so indexpage is available on children
            # when generating this index page
            node.children.each do |c|
                write_index site, c
            end

            index = IndexPage.new(site, node)
            index.render(site.layouts, site.site_payload)
            index.write(site.dest)
            site.pages << index
        end
    end
end
